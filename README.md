# PDF Question Answering API

This FastAPI project allows users to upload PDF documents and query them for answers using a natural language processing model.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Architectural Overview](#architectural-overview)
- [Testing](#testing)

## Setup Instructions

To run this API locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/reyanalam/pdf_question_answer.git
cd pdf_question_answer
```
### 2. Create and activate a virtual environment
```
conda create -p venv
conda activate venv/
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Ensure that the directory for storing uploaded PDFs and FAISS embeddings exists
```
mkdir ./uploads
```
### 5. To run the FastAPI server locally
```
uvicorn src.main:app --reload
```
### 6. Testing
Open a different command prompt, navigate to the test folder, and run:
```
cd src/test
pytest test_api.py
```

## Architectural Overview
This API is designed with the following components:

### 1.FastAPI Application (src.main)
The FastAPI application serves as the core of the API, handling incoming HTTP and WebSocket requests. It includes the following:

#### CORS Middleware: Configured to allow requests from any origin.
#### Endpoints:
/upload_pdf/ for PDF file uploads.
/ws/question/ for handling real-time WebSocket-based question-answering.

### 2.PDF Processing (src.services.pdf_service)
The process_pdf_upload function handles the processing of PDF files:

Extracts text content from uploaded PDFs using the fitz (PyMuPDF) library.
Splits the content into chunks using RecursiveCharacterTextSplitter from Langchain.
Embeds the content using SentenceTransformerEmbeddings and stores the embeddings in a FAISS database.

### 3.FAISS Database (src.services.faiss_db)
FAISS is used to store document embeddings and perform efficient similarity searches. The vector database is stored in-memory during the session.

### 4.NLP Model (src.services.nlp_service)
The answer_question function performs natural language question answering. It uses SentenceTransformerEmbeddings to embed the query and performs a similarity search in the FAISS vector store to retrieve relevant information from the PDF.

### 5.Testing (tests)
The test suite includes tests for:

Uploading PDFs.
WebSocket communication for question answering.
Testing
To test the API, we use the pytest framework with FastAPI’s TestClient.

Example Test Cases:
Test PDF upload: Validates that a PDF file can be uploaded and processed correctly.
Test WebSocket connection: Ensures the WebSocket connection can be established.
Test question answering: Sends a question through the WebSocket and checks the received answer.
Test WebSocket session: Validates that follow-up questions can be sent in a continuous session.




