import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app

app = create_app()

# Export the Flask app for Vercel
if __name__ == "__main__":
    app.run()
else:
    # This is for Vercel serverless
    from flask import Flask
    application = app
