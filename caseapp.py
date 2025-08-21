import os
import streamlit as st
import chromadb

# 🔹 Load ChromaDB for Case Retrieval
CHROMA_PATH = "./case_vector_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
case_collection = chroma_client.get_or_create_collection(name="case_documents")

# 🔹 Function to Retrieve Relevant Cases by IPC Section
def retrieve_relevant_cases(ipc_section):
    """Retrieve case documents where metadata contains the exact IPC section."""
    results = case_collection.get()  # Fetch all stored cases

    retrieved_cases = []
    if "metadatas" in results:
        for meta in results["metadatas"]:
            if "ipc_sections" in meta and ipc_section in meta["ipc_sections"].split(", "):
                retrieved_cases.append({"file_name": meta["file_name"], "path": meta["path"]})

    return retrieved_cases

# 🔹 Streamlit UI for Case Retrieval
st.title("📂 IPC Section Case Search")
st.write("Enter an IPC section to find relevant case documents.")

# User Input
ipc_section = st.text_input("Enter IPC Section (e.g., 498A, 302, 304B):")

if st.button("Search Cases"):
    if ipc_section.strip():
        with st.spinner("Searching for relevant cases..."):
            cases = retrieve_relevant_cases(ipc_section)

        st.subheader(f"📄 Cases Related to IPC Section {ipc_section}")
        
        if cases:
            for case in cases:
                file_path = os.path.abspath(case["path"])
                file_name = case["file_name"]

                with open(file_path, "rb") as file:
                    st.download_button(
                        label=f"📥 Download {file_name}",
                        data=file,
                        file_name=file_name,
                        mime="application/pdf"
                    )
        else:
            st.write("⚠️ No relevant case documents found.")

    else:
        st.warning("Please enter an IPC section to search.")

st.markdown("---")
st.markdown("🔹 Built using **ChromaDB** for legal case retrieval.")
