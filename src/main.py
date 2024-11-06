
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router   

app = FastAPI()

# CORS configuration for HTTP routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# including my API router
app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the PDF Question Answering API"}
