from routes import chat
from accuracy_score.collect_responses import collect_responses, save_responses
from accuracy_score.llm_evaluation import load_chat_responses,evaluate_responses
import uvicorn
from typing import List, Dict, Any
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse

# Initialize the FastAPI application
app = FastAPI()

# Include API routes
app.include_router(chat.router, prefix="/chat", tags=["docs"])


#collecting the response
@app.post("/collect-responses")
async def run_collection():
    """Run the collect_responses process from API"""
    questions = [
        "What is the distribution of employees across departments?",
        "What is the average experience of employees?",
        "Can you recommend candidates for the Sales Manager position?",
        "What is the performance distribution of employees?",
        "What are the key skills required for a Sales Manager?",
        "How many employees have more than 5 years of experience?",
        "What is the average performance rating by department?"
    ]

    reference_answers = [
        "The department distribution shows that Sales has 30%, Marketing has 25%, IT has 20%, HR has 15%, and Finance has 10% of employees.",
        "The average experience of employees is 3.5 years, with a minimum of 1 year and maximum of 8 years.",
        "Based on the criteria, I recommend John Doe (5 years experience, MBTI: ENFJ) and Jane Smith (4 years experience, MBTI: ESTP) for the Sales Manager position.",
        "The performance distribution shows that 40% of employees are rated as Excellent, 35% as Good, 20% as Average, and 5% as Needs Improvement.",
        "Key skills for a Sales Manager include leadership, communication, strategic planning, customer relationship management, and data analysis.",
        "Approximately 25% of employees have more than 5 years of experience in the organization.",
        "The average performance rating by department is: Sales (4.2), Marketing (4.0), IT (4.1), HR (3.9), and Finance (4.0)."
    ]

    responses = collect_responses(questions, reference_answers)

    if responses:
        save_responses(responses, filename="results/chat_responses.json")
        return {"status": "success", "message": "Responses collected and saved", "count": len(responses)}
    else:
        return {"status": "error", "message": "No responses collected"}
    


#evaluating the responses
@app.post("/evaluate")
def evaluate_llm_responses():
    try:
        responses = load_chat_responses()
        metrics = evaluate_responses(responses)
        if not metrics:
            return JSONResponse(status_code=400, content={"status": "error", "message": "No metrics returned"})

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Evaluation completed successfully",
                "metrics": metrics
            }
        )

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"status": "error", "message": str(e)})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Error during evaluation: {str(e)}"})





@app.get("/")
async def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the FastAPI application!"}

# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:3000",
]

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True, workers=4)