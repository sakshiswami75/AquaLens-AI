# AquaLens AI 💧

### AI-Powered Water Footprint Intelligence

AquaLens AI is a sustainability-focused web application that helps users understand the hidden water footprint of everyday products such as rice, coffee, cotton, milk, and chocolate.

It uses **Retrieval-Augmented Generation (RAG)** with a curated water-footprint knowledge base and **IBM Granite AI** to provide grounded and understandable answers to user questions.

---

## 🌱 Problem Statement

Water is embedded in the production of many products we consume every day, but this hidden water usage is difficult for people to understand.

Water-footprint estimates can vary depending on factors such as geographic location, climate, production methods, farming practices, and methodology.

AquaLens aims to make this information easier to understand through a simple AI-powered interface.

---

## 💡 Solution

AquaLens allows users to ask natural-language questions about water footprints and water-saving practices.

### Example Questions

- What is the water footprint of rice?
- Why does cotton use water?
- How can we save water in rice farming?

The system retrieves relevant information from its knowledge base and provides it as context to **IBM Granite AI**, which generates a context-aware response.

Users can also view the retrieved knowledge used to generate the answer.

---

## 🤖 AI & RAG Workflow

```text
User Question
      ↓
Knowledge Retrieval
      ↓
Relevant Knowledge
      ↓
IBM Granite AI
      ↓
Grounded Answer
      ↓
User
```

---

## 🧠 Responsible AI

AquaLens follows responsible AI principles by:

- Communicating that water-footprint values are estimates.
- Avoiding unsupported claims.
- Grounding responses using a curated knowledge base.
- Indicating when the available knowledge is insufficient.
- Avoiding fabricated water-footprint values, recommendations, or sources.

---

## 🌍 SDG Alignment

**Primary SDG:**  
**SDG 6 — Clean Water and Sanitation**

AquaLens promotes awareness of freshwater consumption and water efficiency.

**Secondary SDGs:**

- **SDG 12 — Responsible Consumption and Production**
- **SDG 13 — Climate Action**

---

## 👥 Target Users

- Students and learners
- Sustainability educators
- Environment-conscious consumers
- Agriculture learners
- Researchers
- Sustainability awareness organizations

---

## 🛠️ Technologies Used

- **Python**
- **IBM Granite**
- **IBM watsonx.ai**
- **Retrieval-Augmented Generation (RAG)**
- **LangChain**
- **ChromaDB**
- **FastAPI**
- **React**
- **Vite**
- **JavaScript**
- **CSS**

---

## 🚀 How to Run

### Backend

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.app:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 📚 Knowledge Sources

The AquaLens knowledge base uses information from:

- Water Footprint Network
- FAO AGRIS
- FAO AQUASTAT

Water-footprint values are treated as estimates and may vary depending on production and environmental conditions.

---

## 🎯 Expected Impact

AquaLens aims to make hidden water consumption easier to understand and encourage people to make more informed and sustainable consumption decisions.

---

## 👩‍💻 Project

**AquaLens AI**  
Developed by **Sakshi Swami**  


Developed as part of the **1M1B AI for Sustainability Virtual Internship** in collaboration with **IBM SkillsBuild & AICTE**.

---

## 🔗 GitHub

https://github.com/sakshiswami75/AquaLens-AI
