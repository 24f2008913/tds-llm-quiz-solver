# Project Checklist

Complete this checklist before the evaluation on **Nov 29, 2025 at 3:00 PM IST**

## ✅ Setup & Installation

- [ ] Python 3.9+ installed
- [ ] Git installed
- [ ] Virtual environment created
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install chromium`)
- [ ] `.env` file created and configured
- [ ] System tests passing (`python test_system.py`)

## ✅ Configuration

- [ ] EMAIL set in `.env`
- [ ] SECRET set in `.env` (keep it confidential!)
- [ ] OPENAI_API_KEY or ANTHROPIC_API_KEY set
- [ ] Tested local server (`python app.py`)
- [ ] Verified endpoint responds correctly

## ✅ Code Quality

- [ ] All files created and in correct locations
- [ ] No syntax errors
- [ ] Proper error handling implemented
- [ ] Logging configured
- [ ] Code is readable and documented

## ✅ Testing

- [ ] Local server starts without errors
- [ ] Health endpoint works (`GET /health`)
- [ ] Authentication works (rejects invalid credentials)
- [ ] Demo quiz test successful
- [ ] Timeout handling works
- [ ] Error cases handled gracefully

## ✅ GitHub Repository

- [ ] Repository created on GitHub
- [ ] Repository is PUBLIC (important!)
- [ ] MIT LICENSE file present
- [ ] README.md is comprehensive
- [ ] All code files pushed
- [ ] .gitignore configured (no .env file pushed!)
- [ ] Repository URL ready for form

## ✅ Deployment

- [ ] Chosen deployment platform (Render/Railway/Heroku/etc)
- [ ] Code deployed successfully
- [ ] Environment variables configured on platform
- [ ] HTTPS endpoint is active
- [ ] Endpoint URL tested and working
- [ ] Logs are accessible for debugging

## ✅ Prompt Engineering

- [ ] System prompt created (max 100 chars)
- [ ] User prompt created (max 100 chars)
- [ ] Prompts tested locally
- [ ] Character count verified
- [ ] Strategy documented

## ✅ Google Form Submission

- [ ] Email address
- [ ] Secret string (same as in `.env`)
- [ ] System prompt (max 100 chars)
- [ ] User prompt (max 100 chars)
- [ ] API endpoint URL (HTTPS)
- [ ] GitHub repository URL (public)
- [ ] Form submitted successfully

## ✅ Pre-Evaluation Testing

- [ ] Endpoint responds to POST requests
- [ ] Authentication works (403 for wrong credentials)
- [ ] Quiz solving works end-to-end
- [ ] Handles invalid JSON (400 response)
- [ ] Completes within 3-minute timeout
- [ ] Follows quiz chains correctly
- [ ] Handles errors gracefully

## ✅ Viva Preparation

### Understand Your Architecture
- [ ] Can explain overall system design
- [ ] Know why you chose each library
- [ ] Understand data flow
- [ ] Can explain error handling strategy

### Know Your Code
- [ ] Understand how browser rendering works
- [ ] Can explain LLM integration
- [ ] Know data processing pipeline
- [ ] Understand timeout management

### Design Decisions
- [ ] Why Flask over FastAPI/Django?
- [ ] Why Playwright over Selenium?
- [ ] Why OpenAI/Anthropic?
- [ ] How do you handle edge cases?

### Scalability & Performance
- [ ] Current bottlenecks identified
- [ ] Potential optimizations
- [ ] How to handle concurrent requests
- [ ] Memory and resource management

### Security
- [ ] Credential management approach
- [ ] Input validation strategy
- [ ] Error message handling
- [ ] API key security

## ✅ Final Checks (Day Before Evaluation)

- [ ] Repository is public
- [ ] MIT LICENSE is present
- [ ] Endpoint is accessible via HTTPS
- [ ] Test endpoint one more time
- [ ] Environment variables are correct
- [ ] Logs show no critical errors
- [ ] All documentation is up to date
- [ ] Google Form submission is complete

## 📋 Pre-Evaluation Test Script

Run this the day before:

```powershell
# 1. Test health endpoint
curl https://your-app-url.com/health

# 2. Test invalid credentials (should return 403)
curl -X POST https://your-app-url.com/quiz `
  -H "Content-Type: application/json" `
  -d '{"email":"wrong","secret":"wrong","url":"test"}'

# 3. Test with valid credentials and demo quiz
curl -X POST https://your-app-url.com/quiz `
  -H "Content-Type: application/json" `
  -d '{
    "email":"your-email@example.com",
    "secret":"your-secret",
    "url":"https://tds-llm-analysis.s-anand.net/demo"
  }'

# 4. Verify response comes within reasonable time
# 5. Check logs for any errors
```

## 📅 Timeline

### Now → Nov 28
- [x] Complete setup
- [ ] Test thoroughly
- [ ] Deploy to cloud
- [ ] Submit Google Form

### Nov 28 (Day Before)
- [ ] Final testing
- [ ] Verify all systems working
- [ ] Review documentation
- [ ] Prepare for viva

### Nov 29, 3:00 PM IST (Evaluation)
- [ ] Endpoint ready and monitored
- [ ] Logs accessible
- [ ] Ready to debug if needed

### Post-Evaluation (Viva Day)
- [ ] Review your code
- [ ] Understand design choices
- [ ] Prepare to discuss architecture
- [ ] Be ready for technical questions

## 🚨 Common Issues to Avoid

- ❌ Forgetting to make repository public
- ❌ Missing MIT LICENSE file
- ❌ .env file pushed to GitHub (security risk!)
- ❌ Wrong endpoint URL in form
- ❌ Endpoint not using HTTPS
- ❌ Timeout not handled properly
- ❌ Browser not installed on server
- ❌ Environment variables not set on platform

## ✨ Success Criteria

Your system is ready when:

✅ Repository is public with MIT LICENSE
✅ HTTPS endpoint responds correctly
✅ Authentication works (403 for wrong creds)
✅ Quiz solving completes within 3 minutes
✅ Handles quiz chains correctly
✅ Error handling is robust
✅ Logs are accessible
✅ Google Form submitted
✅ You understand your code for viva

## 📊 Self-Assessment

Rate your confidence (1-5):

- [ ] Setup and installation: ___/5
- [ ] Local testing: ___/5
- [ ] Deployment: ___/5
- [ ] Quiz solving logic: ___/5
- [ ] Error handling: ___/5
- [ ] Prompt engineering: ___/5
- [ ] Viva preparation: ___/5

**Target**: All should be 4 or 5 before evaluation!

## 🎯 Final Status

Date: ___________

- [ ] All technical requirements met
- [ ] All documentation complete
- [ ] Form submitted
- [ ] Ready for evaluation
- [ ] Confident about viva

**Signature**: _________________

---

Good luck! You've got this! 🚀

If all boxes are checked, you're ready for the evaluation.
