import os
from dotenv import load_dotenv

# Load production environment variables
load_dotenv('.env.production')

from backend.api import app

if __name__ == "__main__":
    app.run()
