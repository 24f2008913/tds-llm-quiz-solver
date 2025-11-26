"""
Main Flask Application for LLM Analysis Quiz Solver
"""
import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from quiz_solver import QuizSolver

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
EMAIL = os.getenv('EMAIL')
SECRET = os.getenv('SECRET')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')


@app.route('/quiz', methods=['POST'])
def quiz_endpoint():
    """
    Main endpoint that receives quiz tasks and solves them
    
    Expected JSON payload:
    {
        "email": "student@example.com",
        "secret": "student-secret",
        "url": "https://example.com/quiz-834"
    }
    """
    # Validate JSON first (before try block to catch JSON errors)
    if not request.is_json:
        logger.warning("Invalid request: Not JSON content type")
        return jsonify({"error": "Request must be JSON"}), 400
    
    try:
        data = request.get_json(force=False, silent=False)
    except Exception as json_error:
        logger.warning(f"Invalid JSON payload: {str(json_error)}")
        return jsonify({"error": "Invalid JSON format"}), 400
    
    # Validate data is not None
    if data is None:
        logger.warning("Invalid request: Empty JSON")
        return jsonify({"error": "Empty JSON payload"}), 400
    
    try:
        # Validate required fields
        if not all(k in data for k in ['email', 'secret', 'url']):
            logger.warning("Invalid request: Missing required fields")
            return jsonify({"error": "Missing required fields: email, secret, url"}), 400
        
        # Verify credentials
        if data['email'] != EMAIL or data['secret'] != SECRET:
            logger.warning(f"Invalid credentials: {data.get('email')}")
            return jsonify({"error": "Invalid credentials"}), 403
        
        logger.info(f"Valid request received for URL: {data['url']}")
        
        # Initialize quiz solver and start solving
        solver = QuizSolver()
        result = solver.solve_quiz_chain(data['url'])
        
        return jsonify({
            "status": "success",
            "message": "Quiz solving initiated",
            "result": result
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with basic info"""
    return jsonify({
        "name": "LLM Analysis Quiz Solver",
        "version": "1.0.0",
        "endpoints": {
            "/quiz": "POST - Submit quiz task",
            "/health": "GET - Health check"
        }
    }), 200


if __name__ == '__main__':
    # Validate configuration
    if not EMAIL or not SECRET:
        logger.error("EMAIL and SECRET must be set in environment variables")
        exit(1)
    
    logger.info(f"Starting server on {HOST}:{PORT}")
    logger.info(f"Configured for email: {EMAIL}")
    
    app.run(host=HOST, port=PORT, debug=False)
