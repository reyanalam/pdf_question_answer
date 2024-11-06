from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from src.services.pdf_service import faiss_db

embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
def func(faiss_db):
    faiss_db = faiss_db
async def answer_question(query: str):
    #global faiss_db
    # Embed the query
    query_embedding = embedding_model.embed_query(query)
        
    # Performing similarity search
    if faiss_db is None:
        raise ValueError("FAISs database is not initialized. Please upload a PDF first.")
    similar_docs = faiss_db.similarity_search_by_vector(query_embedding, k=2)  
        
    # Extract and return the most relevant response
    if similar_docs:
        return similar_docs[0].page_content  # Returns the text content of the most relevant document
    else:
        return "No relevant information found for your query."
    

