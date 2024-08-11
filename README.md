# PepSales Transcript Analysis

This project analyzes call transcripts between buyers and sellers to extract and store questions in MongoDB, with APIs to retrieve and rate the questions.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ashok-Kumar9/PepSales.git
   cd pepsales_project

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

   Third-Party Libraries
   Flask==3.0.3: For creating the API endpoints.
   pymongo==4.8.0: For interacting with MongoDB.
   pdfplumber==0.11.3: For extracting text from PDF files.
   anthropic==0.33.0: For integrating with the Anthropic API for advanced analysis.