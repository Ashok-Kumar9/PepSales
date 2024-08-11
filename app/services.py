import os
import re
import pdfplumber
from app.models import Question
from app.llm import process_transcript_with_llm, analyze_questions
import logging
from file_utils import load_json_from_file, save_json_to_file, FOLDER_PATH_FOR_TRANSCRIPTS, FOLDER_PATH_QUESTION_ANALYSIS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_text(text):
    # Remove leading and trailing quotes
    text = text.strip('"')

    # Replace non-breaking spaces with regular spaces
    text = text.replace('\u2026', '...')
    
    # Remove excessive newlines and extra spaces
    text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single newline

    # Extract only the transcript section
    transcript_section = re.search(r'Transcript\n(.*)', text, re.DOTALL)
    
    if transcript_section:
        transcript_section = transcript_section.group(1)
    else:
        transcript_section = text

    # Find all timestamp and dialogue entries
    entries = re.findall(r'(\d{1,2}:\d{2})\s*\|\s*(\w+)\n(.*?)(?=\n\d{1,2}:\d{2}|$)', transcript_section, re.DOTALL)
    
    # Create structured data
    data = {
        'transcript': []
    }
    
    for entry in entries:
        timestamp, speaker, dialogue = entry
        data['transcript'].append({
            'timestamp': timestamp,
            'speaker': speaker,
            'dialogue': dialogue.strip()
        })

    return data

def extract_text_from_pdfs(directory):
    transcripts = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and filename.startswith("abc_call_"):
            logger.info(f"Processing {filename}")
            existing_data = load_json_from_file("extracted_"+filename.replace("pdf", "json"), FOLDER_PATH_FOR_TRANSCRIPTS)
            if existing_data:
                transcripts.append(existing_data)
                continue

            pdf_path = os.path.join(directory, filename)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text()
                    text = format_text(text)
                    transcripts.append(text)
                    save_json_to_file(text, "extracted_"+filename.replace("pdf", "json"), FOLDER_PATH_FOR_TRANSCRIPTS)
                    logger.info(f"Extracted text from {filename}")
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
    return transcripts

def process_transcripts(directory):
    transcripts = extract_text_from_pdfs(directory)
    logger.info(f"Processed {len(transcripts)} transcripts")
    all_questions = []

    for index, transcript in enumerate(transcripts):
        questions = process_transcript_with_llm(transcript, f"questions_abc_call_{index + 1}.json")
        all_questions.extend(questions)

    logger.info(f"Extracted {len(all_questions)} questions")

    save_json_to_file(all_questions, "all_questions.json", FOLDER_PATH_QUESTION_ANALYSIS)

    analyzed_questions = analyze_questions(all_questions)
    print(f"Analyzed {len(analyzed_questions)} questions")

    # Store top 5 questions in the database
    for q in analyzed_questions:
        Question(
            question=q['question'],
            answer=q['answer'],
            rating=q['rating'],
            analysis=q['analysis'],
            count=q['count']
        ).save()

    final_analysis = {
        "Overall Analysis": "Analysis of top 5 questions from all transcripts",
        "total_transcripts": len(transcripts),
        "total_questions": len(all_questions),
        "top_questions": [q for q in analyzed_questions]
    }

    save_json_to_file(final_analysis, "final_analysis.json", FOLDER_PATH_QUESTION_ANALYSIS)
    return final_analysis