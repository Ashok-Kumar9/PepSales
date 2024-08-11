# PepSales Transcript Analysis

This project analyzes call transcripts between buyers and sellers to extract and store questions in MongoDB, with APIs to retrieve and rate the questions.

## Folder and Files - Check the extracted files and final analysis

- **`Extracted Transcripts`:** Stores JSON files of transcripts after processing from PDFs.
- **`Question Data Files`:** Contains the extracted questions from the transcripts.
- **`Question Analysis Files`:** Holds the final analysis results, ratings, and reports for insights.
  - all_questions.json
  - final_analysis.json
  - top_five_questions.json

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ashok-Kumar9/PepSales.git
   cd pepsales_project
   
2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv pepsales_env
    pepsales_env\Scripts\activate #For Windows

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

**Third-Party Libraries**
- Flask==3.0.3: For creating the API endpoints.
- pymongo==4.8.0: For interacting with MongoDB.
- pdfplumber==0.11.3: For extracting text from PDF files.
- anthropic==0.33.0: For integrating with the Anthropic API for advanced analysis.

4. **Run the application:**
   ```bash
   python app/main.py

## API Endpoints
**POST** *http://127.0.0.1:5000/api/process* <br > Process and store questions from transcripts.

## Testing
1. **Update the ANTHROPIC_API_KEY in app/config.py**
   - please contact on +91-9024276892 or ashokkumar9@alumni.iitm.ac.in for temp api-key
 
2. **Delete the below folders, currently these have the data to verify:**
   - Extracted Transcripts
   - Question Data Files
   - Question Analysis Files 
   
4. **Run tests to update the data:**
   ```bash
   python test_api.py

## Mongodb 
<img src="https://github.com/user-attachments/assets/d8c76cae-b03a-4777-8bb4-6407f36ffea8" alt="image" width="756" height="auto">
