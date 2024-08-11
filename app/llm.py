import anthropic
import json
import re
from app.config import Config
from file_utils import save_json_to_file, load_json_from_file, FOLDER_PATH_FOR_TRANSCRIPTS, FOLDER_PATH_QUESTION_DATA, FOLDER_PATH_QUESTION_ANALYSIS, FOLDER_PATH_QUESTION_ANALYSIS

client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

def process_transcript_with_llm(transcript, filename="llm_response.json"):

    # Load data from the file if it exists
    existing_data = load_json_from_file(filename, FOLDER_PATH_QUESTION_DATA)
    if existing_data:
        return existing_data

    system_prompt = (
        "You are an assistant tasked with analyzing sales call transcripts to identify questions and answers exchanged between the buyer and seller in B2B SaaS transactions. "
        "Keep in mind that questions and answers may be context-based, so if needed, generate new questions as well. "
        "Present the findings as a list of JSON objects, with each object containing 'question', 'answer', and 'rating' fields."
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Review the following sales call transcript and identify all the questions posed by the seller. "
                    f"Note that questions may not always be marked by a question mark; they can be more context-based. "
                    f"Remove the questions without answers. "
                    f"Rate each answer contextually: 'Best' if it is highly relevant to the B2B SaaS transaction, "
                    f"'Good' if it pertains to inquiries about specific details, and 'Average' if it is more general, "
                    f"such as questions about name, location, or health. "
                    f"Present the results as a list of JSON objects, with each object containing 'question', 'answer', and 'rating' fields."
                    f"\n\nTranscript: {transcript}\n\nOutput:"
                )
            }
        ]
    )

    # Check if content is a list and join if necessary
    content = message.content
    
    # Extract text from the TextBlock
    text = content[0].text

    # Convert the text to a string
    text_str = str(text)

    # Split the text to remove the first element
    split_text = text_str.split(':\n\n')[1]
    json_objects = re.findall(r'\{[^{}]*\}', split_text)

    # Join the valid JSON objects into a single string
    json_string = '[' + ','.join(json_objects) + ']'

    # Parse the remaining text into a JSON format
    try:
        json_data = json.loads(json_string)
        # Print the JSON data in a beautified format
        save_json_to_file(json_data, filename, FOLDER_PATH_QUESTION_DATA)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def analyze_questions(questions):

    existing_data = load_json_from_file("top_five_questions.json", FOLDER_PATH_QUESTION_ANALYSIS)
    if existing_data:
        return existing_data
    
   
    system_prompt = (
        "You are an assistant that analyzes and evaluates sales questions and answers. "
        "From a list of questions, identify and select the top 5 questions that are most relevant to the conversation "
        "between the buyer and seller in a B2B SaaS context. "
    )


    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
               "content": (
                            f"Analyze the following sales questions and answers from the call transcripts between the buyer and seller in B2B SaaS transactions. "
                            f"For each question-answer pair:\n"
                            f"1. Identify and group all similar questions asked by the seller across the transcripts.\n"
                            f"2. Select the top 5 most relevant questions based on their frequency and importance to the conversation.\n"
                            f"3. Provide a brief analysis of each selected question's effectiveness and rate the corresponding answer as Best, Good, or Average.\n\n"
                            f"Questions and Answers:\n{json.dumps(questions, indent=2)}\n\n"
                            f"Output as a list of JSON objects, each containing 'question', 'count', 'answer', 'analysis', and 'rating' fields."
                        )

            }
        ]
    )


    # Check if content is a list and join if necessary
    content = message.content
    
    # Extract text from the TextBlock
    text = content[0].text

    # Convert the text to a string
    text_str = str(text)

    # Split the text to remove the first element
    split_text = text_str.split(':\n\n')[1]
    json_objects = re.findall(r'\{[^{}]*\}', split_text)

    # Join the valid JSON objects into a single string
    json_string = '[' + ','.join(json_objects) + ']'

    # Parse the remaining text into a JSON format
    try:
        json_data = json.loads(json_string)
        #save_json_to_file(json_data, filename, FOLDER_PATH_QUESTION_ANALYSIS)
        save_json_to_file(json_data, 'top_five_questions.json', FOLDER_PATH_QUESTION_ANALYSIS)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
