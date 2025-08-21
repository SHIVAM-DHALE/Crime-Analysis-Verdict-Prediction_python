import streamlit as st
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

# 🔹 Streamlit Page Configuration
st.set_page_config(page_title="IPC Legal Assistant", layout="wide")

# 🔹 Load Local Embedding Model
embedding_model_path = "./models/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(embedding_model_path)

# 🔹 Load ChromaDB (Vector Database)
ipc_chroma_path = "./vector_db"
case_chroma_path = "./case_vector_db"

ipc_chroma_client = chromadb.PersistentClient(path=ipc_chroma_path)
case_chroma_client = chromadb.PersistentClient(path=case_chroma_path)

ipc_collection = ipc_chroma_client.get_collection(name="ipc_sections")
case_collection = case_chroma_client.get_collection(name="case_documents")

# 🔹 Configure Gemini API
genai.configure(
    api_key="AIzaSyC7W5QsVW63nFJjxf5WnI4jhkmzKqMGEAQ"
)  # Replace with your actual API key
model = genai.GenerativeModel("gemini-2.0-flash")


# 🔹 Function to Retrieve IPC Sections
def retrieve_ipc_sections(query, top_k=3):
    """Retrieve the most relevant IPC sections based on a query."""
    query_embedding = embedding_model.encode(query).tolist()
    results = ipc_collection.query(query_embeddings=[query_embedding], n_results=top_k)

    if results["ids"]:
        retrieved_texts = []
        ipc_numbers = []  # Store only IPC section numbers for case retrieval

        for meta in results["metadatas"][0]:
            section_id = meta["section"].replace("IPC_", "").strip()  # ✅ Remove prefix
            description = meta["description"]
            retrieved_texts.append(f"Section {section_id}: {description}")
            ipc_numbers.append(section_id)  # ✅ Store cleaned IPC numbers

        return retrieved_texts, ipc_numbers
    return ["No relevant IPC section found."], []


# 🔹 Function to Retrieve Case Documents
def retrieve_relevant_cases(ipc_numbers, top_k=3):
    """Retrieve case documents where metadata contains the exact IPC section."""
    all_cases = []

    print(
        "🔍 Searching for cases with IPC Sections:", ipc_numbers
    )  # ✅ Debugging Output

    for ipc_section in ipc_numbers:
        results = case_collection.get()  # Fetch all stored cases

        if "metadatas" in results:
            for meta in results["metadatas"]:
                # ✅ Allow partial match (e.g., "498A" in "498A, 304B, 34")
                if "ipc_sections" in meta and ipc_section in meta["ipc_sections"]:
                    all_cases.append(
                        {"file_name": meta["file_name"], "path": meta["path"]}
                    )

    return all_cases[:top_k]  # Return the top N case documents


# 🔹 Function to Summarize PDF
def summarize_pdf(file_path):
    """Summarize the content of a PDF file in two sentences."""
    reader = PdfReader(file_path)
    content = " ".join(
        page.extract_text() for page in reader.pages[:5]
    )  # Limit to first 5 pages
    prompt = f"Summarize the following legal document in two sentences:\n\n{content}"
    response = model.generate_content(prompt)
    return response.text if response else "Summary not available."


# 🔹 Function to Generate Legal Response
def generate_response(user_query):
    """Generate a legal response using retrieved IPC sections and Gemini API."""
    retrieved_sections, ipc_numbers = retrieve_ipc_sections(user_query)

    # ✅ Ensure clean IPC section numbers
    ipc_numbers = [sec.replace("IPC_", "").strip() for sec in ipc_numbers]

    # 🔹 Print extracted IPC section numbers for debugging
    print("✅ Cleaned IPC Sections for Retrieval:", ipc_numbers)

    # 🔹 Format retrieved sections as input for Gemini
    context = "\n".join(retrieved_sections)
    prompt = f"""Do not apply your own knowledge and use only the provided context. 
    You are a legal assistant. Based on the relevant IPC sections, determine which IPC sections may be applicable to the user and their corresponding punishments.
    Mention the punishments separately.
    User Query: {user_query}
    
    Relevant IPC Sections:
    {context}
    """

    # 🔹 Call Gemini API for LLM response
    response = model.generate_content(prompt)

    return response.text if response else "Error generating response.", ipc_numbers


# 🔹 Streamlit UI
st.title("🔍 IPC Legal Assistant & Case Retrieval")
st.write(
    "Enter a scenario to find relevant IPC sections, legal analysis, and similar past cases."
)

# User Input
user_query = st.text_area(
    "Describe the incident:", placeholder="E.g., I robbed a house"
)

if st.button("Find Applicable IPC Sections & Cases"):
    if user_query.strip():
        with st.spinner("Retrieving legal insights..."):
            response, ipc_numbers = generate_response(user_query)

        st.subheader("📜 Applicable IPC Sections & Analysis")
        st.write(response)

        # 🔹 Retrieve Relevant Case Documents
        if ipc_numbers:
            with st.spinner("Finding relevant cases..."):
                cases = retrieve_relevant_cases(ipc_numbers)

            st.subheader("🗂 Relevant Case Documents")

            if cases:
                for case in cases:
                    file_path = case["path"]
                    file_name = case["file_name"]

                    # Summarize the PDF content
                    summary = summarize_pdf(file_path)

                    st.write(f"**{file_name}**")
                    st.write(f"*Summary:* {summary}")

                    with open(file_path, "rb") as file:
                        st.download_button(
                            label=f"💾 Download {file_name}",
                            data=file,
                            file_name=file_name,
                            mime="application/pdf",
                        )
            else:
                st.write("⚠️ No relevant case documents found.")
        else:
            st.write(
                "⚠️ No IPC sections were identified, so no cases could be retrieved."
            )

    else:
        st.warning("Please enter a scenario to proceed.")

st.markdown("---")
st.markdown("🔹 Built using **local embeddings**, **ChromaDB**, and **Gemini API**.")
