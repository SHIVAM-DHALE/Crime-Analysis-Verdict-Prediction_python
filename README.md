# ⚖️ AI Legal Assistant: IPC Section Predictor & Case Retrieval System

An AI-powered legal assistance tool built with Python that interprets criminal case descriptions, predicts relevant IPC sections and punishments, and retrieves similar past legal cases. Designed to support FIR filing, legal research, and public legal awareness.

---

## 📝 Short Description / Purpose

The **AI Legal Assistant** is a semantic, Python-based NLP tool that transforms unstructured legal queries into actionable legal insights. It predicts the most relevant **Indian Penal Code (IPC) sections**, estimates **legal punishments**, and retrieves **semantically similar case precedents**.

> 🧠 **Bonus Purpose**:  
> This tool also serves as a **legal guide** for the general public. Since remembering all IPC sections, their punishments, and associated cases is impractical for most people, this system provides **easy legal reference and education**.

---

## 🎯 Objective

The core objective of this project is to develop an AI-driven legal assistance system capable of:

1. **Automated IPC Section Classification**  
   Automatically identify applicable IPC sections from natural language crime descriptions, improving legal classification speed and accuracy.

2. **Punishment Estimation Based on Precedents**  
   Predict punishments aligned with historical judicial rulings, ensuring fairness and consistency.

3. **Improved FIR Filing Support**  
   Assist law enforcement in correctly identifying charges during FIR filing, reducing errors and improving documentation accuracy.

4. **Judicial Decision Support System**  
   Provide judges and legal practitioners with relevant IPC references, past rulings, and sentencing patterns.

5. **Semantic Retrieval of Similar Cases**  
   Use NLP to retrieve precedent case documents that match the semantics of the user’s query, offering deeper legal context.

---

## 🧰 Tech Stack

| Component               | Technology/Tool                        |
|------------------------|----------------------------------------|
| **NLP Embeddings**     | SentenceTransformer (all-MiniLM-L6-v2) |
| **Vector Search**      | ChromaDB (cosine similarity)           |
| **Text Preprocessing** | NLTK, custom pipeline                  |
| **PDF Parsing**        | PyPDF2                                 |
| **Summarization**      | Google Gemini API                      |
| **User Interface**     | Streamlit (Python-based UI)            |

---

## 🗂️ Data Source

The dataset consists of **511 structured legal records** curated from:
- Indian Kanoon
- Legislation.gov.in
- Public legal repositories

Each record contains:
- **Offense**: Crime description in legal terms  
- **Punishment**: Corresponding IPC-stated punishment  
- **IPC Section**: Legal section number (e.g., 354, 420)  
- **Judgment PDF**: Extracted legal rulings

### Preprocessing Pipeline:
- PDF to Text (PyPDF2)
- Text Normalization (lowercasing, punctuation removal)
- Tokenization & Stopword Removal (NLTK)
- Embedding Generation (SentenceTransformer)
- Label Encoding (for IPC sections)
- SMOTE & Weighting (for class imbalance handling)

---

## 🚀 Features / Highlights

### 🔎 Key Functionalities

- **IPC Section Prediction**  
  Automatically predicts relevant IPC sections based on crime narratives.

- **Punishment Estimation**  
  Displays potential sentences or fines as per IPC.

- **Case Retrieval**  
  Finds and presents similar past case rulings for reference.

- **AI Case Summarization**  
  Uses Google Gemini API to generate concise summaries of lengthy judgments.

- **User-Friendly Interface**  
  Built with Streamlit, enabling users to input scenarios, view legal outcomes, and download related case PDFs.

-----

![Alt Text](https://i.ibb.co/cK7r1Q2B/Untitled-Diagramresearch.jpg)

## 🔍 Component Contributions

| Component              | Contribution Summary |
|------------------------|----------------------|
| **SentenceTransformer** | Converts crime descriptions and legal texts into semantically meaningful vectors |
| **ChromaDB**            | Performs fast cosine similarity search to retrieve relevant IPC sections and documents |
| **Gemini API**          | Generates readable summaries from complex court documents |
| **PyPDF2**              | Extracts clean, structured text from unstructured legal PDFs |
| **Streamlit UI**        | Enables public interaction with the system in real-time |

---

## 💡 Qualitative Example

**🧾 User Query:**  
> “The man harassed the woman by making vulgar comments and inappropriate gestures in a public place.”

**🔍 System Output:**  
- **Predicted IPC Sections**:
  - **Section 354** – Outraging the modesty of a woman  
  - **Section 354A** – Sexual harassment  
  - **Section 509** – Insulting the modesty of a woman

- **Punishments**:
  - **509**: Up to 3 years imprisonment + fine  
  - **354A**: Up to 1 year or fine or both  
  - **354**: 1 to 5 years imprisonment + fine

- **Extra Features**:
  - 📥 Download related case PDFs  
  - 📄 AI-generated summaries for quicker legal understanding
---
![Alt Text](https://i.ibb.co/fGP3n30T/Screenshot-2025-04-14-125852.png)
![Alt Text](https://i.ibb.co/fzGRz1Vs/Screenshot-2025-04-14-125915.png)
![Alt Text](https://i.ibb.co/60yL4mmk/Screenshot-2025-04-14-125946.png)
![Alt Text](https://i.ibb.co/4wRN9qtd/Screenshot-2025-04-14-130013.png)
