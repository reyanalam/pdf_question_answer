import fitz  # a module under PyMuPDF
import os
from fastapi import UploadFile
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

faiss_db = None
async def process_pdf_upload(file: UploadFile):
    global faiss_db
    upload_dir = "./uploads"   
    pdf_file_path = os.path.join(upload_dir, file.filename)  

    os.makedirs(upload_dir, exist_ok=True)  # Creating a folder to store the PDF
    pdf_content = await file.read()  # Reading the content of the PDF
    
    # Saving PDF
    with open(pdf_file_path, "wb") as f:
        f.write(pdf_content)
    
    # Extracting text
    text = extract_text_from_pdf(pdf_file_path)
    text_document = Document(page_content=text)  # Creating Document instance
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents = text_splitter.split_documents([text_document])  # Splitting into chunks
    
    # Embedding model
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_db = FAISS.from_documents(documents, embedding_model)
    print("FAISS database initialized",faiss_db is not None)
    return {"filename": file.filename, "message": "File uploaded and processed successfully."}

# Creating a function that extracts text from the stored PDF file path
def extract_text_from_pdf(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
