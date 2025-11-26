# LLM Analysis Quiz Solver

An automated system that solves data-related quizzes using LLMs, headless browsing, and data processing capabilities.

## Features

- **API Endpoint**: Flask server accepting POST requests with quiz tasks
- **Headless Browser**: Renders JavaScript-based quiz pages using Playwright
- **LLM Integration**: Uses AI Pipe for cost-effective access to multiple LLM models
- **Data Processing**: Handles PDFs, images, CSV, JSON, and various data formats
- **Automated Submission**: Submits answers with retry logic and timeout handling
- **Visualization**: Generates charts and images as needed

## Setup

### Prerequisites

- Python 3.9+
- Node.js (for Playwright)
- AI Pipe token from https://aipipe.org/login

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd p2
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Create a `.env` file with your configuration:
```bash
cp .env.example .env
```

5. Edit `.env` and add your credentials:
```
EMAIL=your-email@example.com
SECRET=your-secret-string
AIPIPE_TOKEN=your-aipipe-token
PORT=5000
```

## Running the Application

### Local Development

```bash
python app.py
```

The server will start on `http://localhost:5000` (or your configured port).

### Testing

Test your endpoint with the demo quiz:

```bash
curl -X POST http://localhost:5000/quiz \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "secret": "your-secret",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

## Deployment

### Using ngrok (for testing)

```bash
ngrok http 5000
```

Use the HTTPS URL provided by ngrok as your API endpoint.

### Production Deployment Options

- **Heroku**: See `Procfile` for configuration
- **AWS Lambda**: Can be adapted with serverless framework
- **Google Cloud Run**: Containerized deployment
- **Render/Railway**: Easy deployment platforms

## Project Structure

```
p2/
├── app.py                  # Main Flask application
├── quiz_solver.py          # Quiz solving logic
├── browser_handler.py      # Headless browser operations
├── data_processor.py       # Data processing utilities
├── llm_handler.py          # LLM interaction logic
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
├── LICENSE                 # MIT License
└── README.md               # This file
```

## How It Works

1. **Receive Request**: API endpoint receives POST request with quiz URL
2. **Validate**: Checks email and secret match configuration
3. **Fetch Quiz**: Uses headless browser to render JavaScript page
4. **Parse Question**: Extracts quiz instructions and requirements
5. **Process Data**: Downloads files, processes PDFs, analyzes data
6. **Generate Answer**: Uses LLM to understand and solve the task
7. **Submit**: Posts answer to specified endpoint within 3 minutes
8. **Iterate**: If there's a next URL, repeats the process

## Prompt Engineering

### System Prompt (Max 100 chars)
Designed to resist revealing code words through instruction hierarchy and obfuscation.

### User Prompt (Max 100 chars)
Designed to bypass system prompts using jailbreak techniques and social engineering.

## License

MIT License - see LICENSE file for details

## Author

Built for the TDS LLM Analysis Quiz Project
