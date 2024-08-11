from flask import Blueprint, jsonify, request
from app.services import process_transcripts

api_bp = Blueprint('api', __name__)

@api_bp.route('/process', methods=['POST'])
def process_transcripts_route():
    try:
        transcript_dir = request.json.get('transcript_dir')
        if not transcript_dir:
            return jsonify({"error": "transcript_dir is required"}), 400
        result = process_transcripts(transcript_dir)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500