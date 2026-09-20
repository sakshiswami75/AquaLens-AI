import os
from dotenv import load_dotenv
import chromadb
from fastembed import TextEmbedding
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")


# ==========================================
# 2. Load knowledge base
# ==========================================

loader = TextLoader(
    "data/water_footprint_notes.txt",
    encoding="utf-8"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

texts = [chunk.page_content for chunk in chunks]


# ==========================================
# 3. Create embeddings
# ==========================================

embedding_model = TextEmbedding()

embeddings = list(
    embedding_model.embed(texts)
)


# ==========================================
# 4. Connect to ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="aqualens_knowledge"
)

# Get existing IDs
existing = collection.get()
existing_ids = set(existing["ids"])

# Add only new chunks
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
# 5. Get question from user
# ==========================================

question = input(
    "\nAsk AquaLens a question: "
)


# ==========================================
# 6. Retrieve relevant knowledge
# ==========================================

question_embedding = list(
    embedding_model.embed([question])
)[0]

results = collection.query(
    query_embeddings=[
        question_embedding.tolist()
    ],
    n_results=5
)

retrieved_information = "\n\n".join(
    results["documents"][0]
)

print("\nRetrieved information:")
print(retrieved_information)


# ==========================================
# 7. Connect to IBM Granite
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
# 8. Ask Granite using retrieved context
# ==========================================

prompt = f"""
You are AquaLens AI, a responsible sustainability assistant.

STRICT RULES:
1. Use ONLY the information in the Knowledge Base.
2. Do NOT add facts, examples, practices, numbers, or
recommendations that are not explicitly stated there.
3. Do NOT use your general knowledge.
4. If the Knowledge Base does not answer the question,
say: "The available knowledge base does not contain
enough information to answer this question."
5. Do not make assumptions.
6. Keep the answer clear and concise.

Knowledge Base:
{retrieved_information}

User Question:
{question}

Answer:
"""
response = model.generate_text(
    prompt=prompt,
    params={
        "max_new_tokens": 200
    }
)


# ==========================================
# 9. Display answer
# ==========================================

print("\nAquaLens AI:")
print(response)