
import os
import json
from typing import List, Dict, Any
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
import sacrebleu

def load_chat_responses():
    """Load chat responses from a JSON file."""
    try:
        with open('results/chat_responses.json', 'r') as f:
            responses = json.load(f)
            return responses
    except Exception as e:
        print(f"Error loading chat responses: {str(e)}")
        return None




def evaluate_responses(responses: List[Dict[str, Any]]):
    """Evaluate responses with BLEU and ROUGE metrics."""
    for response in responses:
          reference = response.get('reference', '')
          candidate = response.get('candidate', '')
    bleu = sacrebleu.corpus_bleu([candidate], [[reference]])
    return bleu.score



