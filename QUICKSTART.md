# Quick Start Guide

Get your LLM Quiz Solver running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Git
- An OpenAI or Anthropic API key

## Installation (Windows)

### Option 1: Automated Setup (Recommended)

```powershell
# Run the setup script
.\setup.ps1
```

This will:
- Create a virtual environment
- Install all dependencies
- Install Playwright browsers
- Create .env file

### Option 2: Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Setup environment
copy .env.example .env
```

## Configuration

Edit `.env` file with your details:

```env
EMAIL=your-email@example.com
SECRET=your-unique-secret-string
OPENAI_API_KEY=sk-...your-key...
```

**Important**: Keep your secret string confidential!

## Testing

Test your setup:

```powershell
python test_system.py
```

All tests should pass ✓

## Running Locally

Start the server:

```powershell
python app.py
```

You should see:
```
Starting server on 0.0.0.0:5000
Configured for email: your-email@example.com
```

## Test Your Endpoint

In another terminal:

```powershell
# Test with demo quiz
curl -X POST http://localhost:5000/quiz `
  -H "Content-Type: application/json" `
  -d '{
    "email": "your-email@example.com",
    "secret": "your-secret",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

## Deployment

### Quick Deploy to Render.com

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repo
   - Configure:
     - Build: `pip install -r requirements.txt && playwright install chromium`
     - Start: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`
   - Add environment variables (EMAIL, SECRET, OPENAI_API_KEY)
   - Deploy!

3. **Get your URL**
   ```
   https://your-app-name.onrender.com
   ```

## Submit to Google Form

Fill the form with:
- Your email
- Your secret string
- System prompt (max 100 chars) - see PROMPTS.md
- User prompt (max 100 chars) - see PROMPTS.md
- API endpoint: `https://your-app-name.onrender.com/quiz`
- GitHub repo URL (must be public with MIT LICENSE)

## Troubleshooting

### "Module not found"
```powershell
pip install -r requirements.txt
```

### "Playwright not installed"
```powershell
playwright install chromium
```

### "Invalid credentials"
Check your `.env` file matches the request payload

### "Timeout"
Quiz must complete within 3 minutes. Check:
- LLM API response time
- Network connectivity
- File download sizes

## Next Steps

1. ✅ Setup complete
2. ✅ Local testing successful
3. ✅ Deployed to cloud
4. ✅ Submitted Google Form
5. 📅 Wait for evaluation (Nov 29, 3 PM IST)
6. 🎤 Prepare for viva

## Resources

- **DEPLOYMENT.md** - Detailed deployment guide
- **PROMPTS.md** - Prompt engineering tips
- **ARCHITECTURE.md** - System architecture
- **README.md** - Complete documentation

## Tips for Success

### Before Evaluation (Nov 29)

- [ ] Test your endpoint multiple times
- [ ] Verify it handles edge cases
- [ ] Ensure 3-minute timeout works
- [ ] Check logs are accessible
- [ ] Test with different quiz scenarios
- [ ] Prepare for viva questions

### Viva Preparation

Understand:
- Why you chose specific libraries
- How LLM integration works
- Your error handling strategy
- Scalability considerations
- Security measures

### Common Viva Questions

1. "Why did you use Playwright instead of Selenium?"
2. "How do you handle timeout in quiz chains?"
3. "What happens if the LLM returns an invalid answer?"
4. "How would you scale this to 1000 concurrent users?"
5. "What security measures did you implement?"

## Support

If you encounter issues:

1. Check logs: `heroku logs --tail` (or platform equivalent)
2. Review error messages
3. Consult DEPLOYMENT.md troubleshooting
4. Test components individually with test_system.py

## Good Luck! 🚀

You're ready for the quiz evaluation!

Remember:
- Your endpoint must be accessible via HTTPS
- Must respond within 3 minutes
- Must handle the quiz chain correctly
- Must have public GitHub repo with MIT LICENSE
