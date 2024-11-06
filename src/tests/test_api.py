import pytest
from fastapi.testclient import TestClient
from src.main import app
from fpdf import FPDF
import os

client = TestClient(app)

@pytest.fixture
def create_test_pdf(tmpdir):
    """Create a simple PDF file for testing in a temporary directory."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test PDF", ln=True, align='C')
    pdf_file_path = tmpdir.join("test.pdf")
    pdf.output(str(pdf_file_path))
    return str(pdf_file_path)

def test_upload_pdf(create_test_pdf):
    """Test the PDF upload endpoint with a valid PDF."""
    with open(create_test_pdf, "rb") as pdf_file:
        response = client.post("/upload_pdf/", files={"file": ("test.pdf", pdf_file)})
    assert response.status_code == 200
    assert "filename" in response.json()


def test_websocket_connection():
    """Test WebSocket connection establishment."""
    websocket = client.websocket_connect("/ws/question/")
    assert websocket  # Ensure the connection was established
    websocket.close()

def test_websocket_question_answer():
    """Test sending a question and receiving an answer via WebSocket."""
    websocket = client.websocket_connect("/ws/question/")
    question = "What is my name?"
    websocket.send_text(question)
    response = websocket.receive_text()
    assert response == "Reyan"  
    websocket.close()

def test_websocket_invalid_question():
    """Test sending an invalid question and handling the response."""
    websocket = client.websocket_connect("/ws/question/")
    question = ""
    websocket.send_text(question)
    response = websocket.receive_text()
    assert response == "Error: Question cannot be empty."  
    websocket.close()

def test_websocket_session_follow_up():
    """Test sending follow-up questions within a session."""
    websocket = client.websocket_connect("/ws/question/")
    websocket.send_text("Tell me about Python.")
    response = websocket.receive_text()
    assert response  # Ensure some response is received

    # Send a follow-up question
    websocket.send_text("What about its libraries?")
    follow_up_response = websocket.receive_text()
    assert follow_up_response  # Ensure some response is received
    websocket.close()
