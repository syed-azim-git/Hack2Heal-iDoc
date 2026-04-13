import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Fine-tuned AI Model Configuration
    MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT', 'http://localhost:8000/api/model')
    MODEL_API_KEY = os.getenv('MODEL_API_KEY', '')
    
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'viberehab')
    
    # Server
    PORT = int(os.getenv('PORT', 5000))

