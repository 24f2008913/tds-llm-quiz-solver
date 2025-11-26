# Architecture Documentation

## System Overview

The LLM Analysis Quiz Solver is a microservice architecture that combines headless browsing, LLM reasoning, and data processing to automatically solve data-related quizzes.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        External System                          │
│                  (Quiz Task Dispatcher)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ POST /quiz
                         │ {email, secret, url}
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Flask API Server                          │
│                         (app.py)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Authentication & Validation                              │  │
│  │  - Verify email/secret                                    │  │
│  │  - Validate JSON payload                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Quiz Solver                                │
│                   (quiz_solver.py)                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Quiz Chain Manager                                       │  │
│  │  - Manages quiz sequence                                  │  │
│  │  - Handles timeout (3 min)                                │  │
│  │  - Coordinates components                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└───┬────────────────┬────────────────┬────────────────┬──────────┘
    │                │                │                │
    ▼                ▼                ▼                ▼
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────────┐
│ Browser │   │   LLM    │   │   Data   │   │     Utils       │
│ Handler │   │ Handler  │   │Processor │   │   (helpers)     │
└─────────┘   └──────────┘   └──────────┘   └─────────────────┘
    │              │              │
    │              │              │
    ▼              ▼              ▼
Playwright    OpenAI/         Pandas/NumPy/
Chromium     Anthropic        PDF/CSV/Excel
                              Processing
```

## Component Details

### 1. Flask API Server (`app.py`)

**Responsibilities:**
- Expose REST API endpoint `/quiz`
- Validate incoming requests
- Authenticate using email/secret
- Route to quiz solver
- Return responses

**Endpoints:**
- `POST /quiz` - Main quiz endpoint
- `GET /health` - Health check
- `GET /` - API info

**Security:**
- Environment-based credentials
- JSON validation
- HTTP status codes (400, 403, 500)

### 2. Quiz Solver (`quiz_solver.py`)

**Responsibilities:**
- Orchestrate the quiz-solving process
- Manage quiz chains (multiple questions)
- Track timeout (3 minutes)
- Parse quiz pages
- Generate answers
- Submit answers

**Key Methods:**
- `solve_quiz_chain()` - Main entry point
- `solve_single_quiz()` - Solve one question
- `parse_quiz_page()` - Extract question details
- `solve_question()` - Generate answer
- `submit_answer()` - POST answer to endpoint

**Flow:**
1. Receive initial quiz URL
2. Loop until no more URLs or timeout:
   - Fetch and render page
   - Parse question and extract data
   - Analyze with LLM
   - Process any data files
   - Generate answer
   - Submit answer
   - Get next URL if correct

### 3. Browser Handler (`browser_handler.py`)

**Responsibilities:**
- Manage headless Playwright browser
- Render JavaScript pages
- Download files
- Extract content
- Take screenshots

**Key Features:**
- Context manager for resource cleanup
- Wait for page rendering
- Extract text, HTML, links
- Base64 decoding support

**Technologies:**
- Playwright (Chromium)
- BeautifulSoup for parsing

### 4. LLM Handler (`llm_handler.py`)

**Responsibilities:**
- Interface with OpenAI and Anthropic APIs
- Analyze quiz questions
- Generate answers
- Format responses

**Key Methods:**
- `generate_completion()` - Get LLM response
- `analyze_quiz_question()` - Understand task
- `generate_answer()` - Create final answer

**Supported Models:**
- OpenAI: GPT-4, GPT-3.5
- Anthropic: Claude 3

**Features:**
- JSON mode for structured output
- Temperature control
- Token limit management
- Multi-provider support

### 5. Data Processor (`data_processor.py`)

**Responsibilities:**
- Download files from URLs
- Process multiple data formats
- Perform data analysis
- Create visualizations
- Web scraping

**Supported Formats:**
- PDF (text + tables)
- CSV
- Excel (XLSX)
- JSON
- Images

**Processing Capabilities:**
- Table extraction
- Data cleaning
- Statistical analysis
- Chart generation
- Base64 encoding

**Libraries:**
- Pandas for data manipulation
- PDFPlumber for PDF parsing
- Matplotlib/Seaborn for viz
- Requests for downloads

### 6. Utilities (`utils.py`)

**Helper Functions:**
- Filename sanitization
- String hashing
- Text truncation
- Number extraction
- JSON save/load
- Retry logic
- Timing

## Data Flow

### Typical Request Flow

1. **Request Reception**
   ```
   External System → Flask (/quiz endpoint)
   ```

2. **Authentication**
   ```
   Flask → Validate email/secret → 200/403
   ```

3. **Quiz Fetching**
   ```
   QuizSolver → BrowserHandler → Render JS page
   ```

4. **Question Analysis**
   ```
   QuizSolver → LLMHandler → Analyze task type
   ```

5. **Data Processing** (if needed)
   ```
   QuizSolver → DataProcessor → Download & process files
   ```

6. **Answer Generation**
   ```
   QuizSolver → LLMHandler → Generate answer
   ```

7. **Answer Submission**
   ```
   QuizSolver → HTTP POST → Submit endpoint
   ```

8. **Next Question** (if available)
   ```
   QuizSolver → Repeat from step 3
   ```

## Error Handling

### Strategy
- Try-catch blocks at each major operation
- Logging at all levels
- Graceful degradation
- Timeout management

### Error Types
- **400 Bad Request**: Invalid JSON
- **403 Forbidden**: Invalid credentials
- **500 Internal Error**: Processing failure

### Recovery
- Retry logic for network operations
- Fallback to alternative data processing
- Continue to next quiz on error

## Performance Considerations

### Bottlenecks
1. **Browser rendering** (2-3 seconds per page)
2. **LLM API calls** (1-5 seconds)
3. **File downloads** (variable)
4. **PDF processing** (1-2 seconds per page)

### Optimizations
- Headless browser reduces overhead
- Concurrent operations where possible
- Efficient data structures
- Token limit awareness

### Timeout Management
- 3-minute hard limit
- Track elapsed time
- Skip to next on failure option

## Scalability

### Current Limitations
- Single-threaded processing
- Synchronous operations
- Memory constraints with large files

### Future Improvements
- Async/await for I/O operations
- Queue system for multiple requests
- Caching for repeated data
- Distributed processing

## Security

### Current Measures
- Environment variables for secrets
- HTTPS for deployment
- Input validation
- No secret logging

### Best Practices
- Regular key rotation
- Minimal permissions
- Request validation
- Error message sanitization

## Monitoring & Debugging

### Logging Levels
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Failures with traces

### Key Metrics
- Request count
- Success/failure rate
- Average response time
- Error types

### Debug Mode
Set in Flask for detailed logs:
```python
app.run(debug=True)  # Development only
```

## Testing Strategy

### Unit Tests
- Individual component functions
- Mock external APIs
- Edge cases

### Integration Tests
- Full request flow
- Multiple quiz chain
- Error scenarios

### System Tests
- `test_system.py` validates:
  - Environment config
  - Package installation
  - Browser setup
  - LLM connectivity
  - Flask endpoints

## Deployment Considerations

### Requirements
- Python 3.9+
- Playwright browsers
- Environment variables
- HTTPS endpoint

### Platforms
- Render.com (recommended)
- Railway
- Heroku
- Google Cloud Run
- AWS Lambda (with adaptation)

### Resource Needs
- **Memory**: 512MB - 1GB
- **Storage**: 500MB (for Chromium)
- **CPU**: 1 vCPU minimum
- **Bandwidth**: Moderate

## Configuration Management

### Environment Variables
All configs via `.env`:
- Credentials
- API keys
- Model selection
- Timeouts
- Ports

### Flexibility
- Easy model switching
- Adjustable timeouts
- Configurable endpoints

## Extension Points

### Adding New Data Formats
1. Add processor in `data_processor.py`
2. Update analysis logic
3. Test with sample data

### Adding New LLM Providers
1. Add client in `llm_handler.py`
2. Implement completion method
3. Update model selection logic

### Adding New Analysis Types
1. Extend `analyze_quiz_question()`
2. Add specialized processors
3. Update answer generation

## Maintenance

### Regular Tasks
- Update dependencies
- Rotate API keys
- Monitor logs
- Review performance

### Troubleshooting
See DEPLOYMENT.md for common issues

## Version History

- **v1.0.0** (2025-11-26): Initial implementation
  - Core quiz solving
  - Multi-format data processing
  - LLM integration
  - Deployment ready
