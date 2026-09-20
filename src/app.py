import os
from dotenv import load_dotenv
import chromadb
from fastembed import TextEmbedding
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================================
# Setup
# ==========================================

load_dotenv()

app = FastAPI(title="AquaLens AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")


# ==========================================
# Load knowledge base
# ==========================================

loader = TextLoader(
    "data/water_footprint_notes.txt",
    encoding="utf-8"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

texts = [chunk.page_content for chunk in chunks]


# ==========================================
# Embeddings + ChromaDB
# ==========================================

embedding_model = TextEmbedding()

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="aqualens_knowledge"
)

existing = collection.get()
existing_ids = set(existing["ids"])

embeddings = list(
    embedding_model.embed(texts)
)

new_ids = []
new_documents = []
new_embeddings = []

for i, (text, embedding) in enumerate(
    zip(texts, embeddings)
):
    chunk_id = f"chunk_{i}"

    if chunk_id not in existing_ids:
        new_ids.append(chunk_id)
        new_documents.append(text)
        new_embeddings.append(
            embedding.tolist()
        )

if new_ids:
    collection.add(
        ids=new_ids,
        documents=new_documents,
        embeddings=new_embeddings
    )


# ==========================================
# IBM Granite
# ==========================================

credentials = Credentials(
    url=WATSONX_URL,
    api_key=API_KEY
)

model = Model(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID
)


# ==========================================
# API model
# ==========================================

class QuestionRequest(BaseModel):
    question: str


# ==========================================
# Routes
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AquaLens AI backend is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "answer": "Please enter a question."
        }

    # Create question embedding
    question_embedding = list(
        embedding_model.embed([question])
    )[0]

    # Retrieve relevant knowledge
    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=1
    )

    retrieved_information = (
        results["documents"][0][0]
    )

    # Grounded prompt
    prompt = f"""
You are AquaLens AI, a responsible sustainability assistant.

STRICT RULES:
1. Use ONLY the information in the Knowledge Base.
2. Do NOT add facts, numbers, examples, recommendations,
or information from your pretrained knowledge that are not
explicitly stated in the Knowledge Base.
3. Do NOT use your general knowledge.
4. If the Knowledge Base does not answer the
question, say that the available knowledge base
does not contain enough information.
5. Keep the answer clear and concise.

Knowledge Base:
{retrieved_information}

User Question:
{question}

Answer:
"""

    response = model.generate_text(
    prompt,
    params={
        "max_new_tokens": 300,
        "temperature": 0
    }
)

    return {
        "question": question,
        "answer": response,
        "source": retrieved_information
    }