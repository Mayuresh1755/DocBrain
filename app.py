import io
import streamlit as st
import os
from pypdf import PdfReader
from dotenv import load_dotenv

# LangChain Imports (Updated)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.question_answering import load_qa_chain

# =========================
# 1. Setup & Config
# =========================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# IMPORTANT: Set API key properly
os.environ["GOOGLE_API_KEY"] = api_key

st.set_page_config(page_title="Enterprise Doc Brain", layout="wide")
st.header("🏢 Multi-Document Knowledge Brain")

# =========================
# 2. Extract Text from PDFs
# =========================
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_stream = io.BytesIO(pdf.read())
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        except Exception as e:
            st.error(f"Error reading {pdf.name}: {e}")
    return text

# =========================
# 3. Split Text into Chunks
# =========================
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return text_splitter.split_text(text)

# =========================
# 4. Create Vector Store
# =========================
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"   # ✅ FIXED MODEL
    )

    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# =========================
# 5. RAG Chain Setup
# =========================
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the context, say:
    "The answer is not available in the documents."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",   # ✅ UPDATED
        temperature=0.3
    )

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# =========================
# 6. Handle User Query
# =========================
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"   # ✅ SAME MODEL
    )

    if os.path.exists("faiss_index"):
        db = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = db.similarity_search(user_question)

        chain = get_conversational_chain()
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )

        st.subheader("🤖 AI Answer:")
        st.write(response["output_text"])

        # OPTIONAL: Show retrieved chunks (for demo)
        with st.expander("🔍 Retrieved Context"):
            for doc in docs:
                st.write(doc.page_content)

    else:
        st.error("⚠️ Please upload and process documents first!")

# =========================
# 7. Sidebar UI
# =========================
with st.sidebar:
    st.title("📁 Document Control")

    pdf_docs = st.file_uploader(
        "Upload PDFs",
        accept_multiple_files=True
    )

    if st.button("Submit & Process"):
        if pdf_docs:
            with st.spinner("Processing documents..."):
                raw_text = get_pdf_text(pdf_docs)

                if raw_text.strip() == "":
                    st.error("❌ No text found in PDFs (maybe scanned files).")
                else:
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("✅ Documents indexed successfully!")

        else:
            st.warning("⚠️ Please upload at least one PDF.")

# =========================
# 8. Main Chat Input
# =========================
user_question = st.text_input("💬 Ask a question about your documents:")
st.write("Using embedding model: text-embedding-004")

if user_question:
    user_input(user_question)