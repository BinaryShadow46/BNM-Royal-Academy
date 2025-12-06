import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bnm-royal-academy-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://root:password@localhost/bnm_royal_academy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # School Information
    SCHOOL_NAME = "BNM ROYAL ACADEMY"
    SCHOOL_ADDRESS = "123 Royal Street, Academic City"
    SCHOOL_PHONE = "+1 234-567-8900"
    SCHOOL_EMAIL = "info@bnmroyalacademy.edu"
