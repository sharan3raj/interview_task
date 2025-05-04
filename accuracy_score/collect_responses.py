import json
import os
import sys
from typing import List, Dict, Any

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

try:
    from services.chat_service import ChatService
except ImportError as e:
    print(f"Error importing ChatService: {str(e)}")
    print("Please ensure you are running the script from the correct directory")
    sys.exit(1)

def collect_responses(questions: List[str], reference_answers: List[str]) -> List[Dict[str, Any]]:
    """Collect responses from the chat service for evaluation."""
    try:
        chat_service = ChatService()
    except Exception as e:
        print(f"Error initializing ChatService: {str(e)}")
        return []
        
    responses = []
    
    for question, reference in zip(questions, reference_answers):
        try:
            # Get response from chat service
            result = chat_service.get_response(question)
            print("result>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", result)
            
            # Extract the answer from the result
            candidate = result.get('answer', '')
            if isinstance(candidate, dict):
                # If answer is a dictionary, convert to string
                candidate = json.dumps(candidate)
            
            # Store the response with additional metadata
            responses.append({
                'question': question,
                'reference': reference,
                'candidate': candidate,
                # 'source_documents': result.get('source_documents', []),
                # 'chat_history': result.get('chat_history', [])
            })
        except Exception as e:
            print(f"Error processing question '{question}': {str(e)}")
    
    # Save the responses after processing all questions
    save_responses(responses, filename='results/chat_responses.json')
    return responses

def save_responses(responses: List[Dict[str, Any]], filename: str = 'results/chat_responses.json'):
    """Save collected responses to a JSON file."""
    try:
        # Ensure the directory exists
        dir_path = os.path.dirname(filename)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # Write responses to the specified file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(responses, f, indent=2, ensure_ascii=False)

        print(f"Responses saved to {filename}")
    except Exception as e:
        print(f"Error saving responses: {str(e)}")
