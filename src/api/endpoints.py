#This code sets up a FastAPI route for handling PDF file uploads

from fastapi import APIRouter, File, UploadFile
from src.services.pdf_service import process_pdf_upload
from fastapi import WebSocket
from src.services.nlp_service import answer_question
from fastapi import HTTPException

#Initializing APIRouter class , this will help in grouping the end points
router = APIRouter()

#defining a POST endpoint
@router.post("/upload_pdf/")

#defining an asynchronous function for file upload and sending it to a process_pdf_upload function
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF file.")
    return await process_pdf_upload(file)

#defining websocket endpoint
@router.websocket("/ws/question/")
#building a function to handle the websocket communication
async def websocket_question_answer(websocket: WebSocket):
    
    await websocket.accept() #accepting the incoming websocket communication
    while True:  #while loop, so that the connection remains open and continuaslly listens for messages from the client.
        
        data = await websocket.receive_text()  #awaiting for text messages from client
        answer = await answer_question(data)  #processing the received message from the client
        await websocket.send_text(answer)   #sending the message back to the client 


