import os
import json

# Define the folder path
FOLDER_PATH_FOR_TRANSCRIPTS = 'Extracted Transcripts'
FOLDER_PATH_QUESTION_DATA = 'Question Data Files'
FOLDER_PATH_QUESTION_ANALYSIS = 'Question Analysis Files'

def save_json_to_file(data, filename, folderpath):
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    
    file_path = os.path.join(folderpath, filename)
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Data successfully saved to {file_path}.")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def load_json_from_file(filename, folderpath):
    file_path = os.path.join(folderpath, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading data from file: {e}")
            return None
    else:
        print(f"File {file_path} does not exist.")
        return None
