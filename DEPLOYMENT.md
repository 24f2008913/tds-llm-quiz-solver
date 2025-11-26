# Deployment Guide

## Quick Deployment Options

### Option 1: Render.com (Recommended)

1. Push your code to GitHub
2. Go to [Render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: llm-quiz-solver (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`
6. Add Environment Variables:
   - `EMAIL`: your email
   - `SECRET`: your secret
   - `OPENAI_API_KEY`: your OpenAI key
   - `ANTHROPIC_API_KEY`: your Anthropic key (optional)
7. Click "Create Web Service"
8. Your URL will be: `https://your-app-name.onrender.com`

### Option 2: Railway.app

1. Push code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables (same as above)
6. Railway will auto-detect Python and deploy
7. Get your URL from the deployment

### Option 3: Heroku

1. Install Heroku CLI: `https://devcenter.heroku.com/articles/heroku-cli`

2. Login and create app:
```bash
heroku login
heroku create your-app-name
```

3. Add buildpacks:
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/mxschmitt/heroku-playwright-buildpack
```

4. Set environment variables:
```bash
heroku config:set EMAIL=your-email@example.com
heroku config:set SECRET=your-secret
heroku config:set OPENAI_API_KEY=your-key
```

5. Deploy:
```bash
git push heroku main
```

6. Your URL: `https://your-app-name.herokuapp.com`

### Option 4: ngrok (Local Testing)

For testing locally with a public URL:

```bash
# Start your Flask app
python app.py

# In another terminal
ngrok http 5000
```

Use the HTTPS URL provided (e.g., `https://abc123.ngrok.io`)

**Note**: ngrok URLs change each session unless you have a paid plan.

### Option 5: Google Cloud Run

1. Install gcloud CLI
2. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

ENV PORT=8080
CMD exec gunicorn app:app --bind :$PORT --timeout 300
```

3. Deploy:
```bash
gcloud run deploy llm-quiz-solver \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars EMAIL=your-email,SECRET=your-secret,OPENAI_API_KEY=your-key
```

### Option 6: AWS Lambda (Advanced)

Requires serverless framework and some code adaptation. Best for production at scale.

---

## Environment Variables Checklist

Before deploying, ensure you have:

- ✅ `EMAIL` - Your email address
- ✅ `SECRET` - Your secret string
- ✅ `OPENAI_API_KEY` - OpenAI API key (if using GPT models)
- ✅ `ANTHROPIC_API_KEY` - Anthropic API key (if using Claude models)
- ⚙️ `PORT` - Usually auto-set by platform (default: 5000)
- ⚙️ `DEFAULT_MODEL` - Optional (default: gpt-4-turbo-preview)

---

## Testing Your Deployment

After deployment, test your endpoint:

```bash
# Health check
curl https://your-app-url.com/health

# Test quiz endpoint (will fail auth)
curl -X POST https://your-app-url.com/quiz \
  -H "Content-Type: application/json" \
  -d '{"email":"wrong","secret":"wrong","url":"test"}'

# Should return 403

# Test with correct credentials
curl -X POST https://your-app-url.com/quiz \
  -H "Content-Type: application/json" \
  -d '{
    "email":"your-email@example.com",
    "secret":"your-secret",
    "url":"https://tds-llm-analysis.s-anand.net/demo"
  }'
```

---

## Monitoring and Logs

### Render
- View logs in dashboard under "Logs" tab
- Enable auto-deploy on git push

### Railway
- Logs available in deployment view
- Set up GitHub auto-deploy

### Heroku
```bash
heroku logs --tail
```

### Google Cloud Run
```bash
gcloud logging read "resource.type=cloud_run_revision"
```

---

## Troubleshooting

### "Playwright not installed"
- Ensure build command includes: `playwright install chromium`
- Add playwright system dependencies if on container

### "Module not found"
- Check requirements.txt is complete
- Verify build logs for installation errors

### "Timeout errors"
- Increase timeout in Procfile/start command
- Check if platform has execution time limits

### "Out of memory"
- Playwright can be memory-intensive
- Upgrade to larger instance/plan
- Consider headless browser alternatives for simple tasks

---

## Cost Considerations

- **Render Free Tier**: Sleeps after 15 min inactivity, good for testing
- **Railway**: $5 free credit/month, then pay as you go
- **Heroku Free**: Discontinued, need paid plan
- **Google Cloud Run**: Pay per request, generous free tier
- **ngrok**: Free for testing, paid for persistent URLs

**Recommendation**: Render.com for simplicity, Google Cloud Run for production.

---

## Security Best Practices

1. **Never commit `.env` file** - Already in .gitignore
2. **Use environment variables** - Not hardcoded secrets
3. **HTTPS only** - All platforms provide this
4. **Validate inputs** - Already implemented in app.py
5. **Rate limiting** - Consider adding if needed
6. **API key rotation** - Regularly update keys

---

## Pre-Evaluation Checklist

Before Nov 29, 3:00 PM IST:

- [ ] Code pushed to public GitHub repo
- [ ] MIT LICENSE file present
- [ ] Application deployed and accessible via HTTPS
- [ ] Environment variables configured
- [ ] Test endpoint with demo quiz
- [ ] Submit Google Form with all details
- [ ] Verify endpoint URL is correct in form
- [ ] Test that endpoint responds within 3 minutes
- [ ] Check logs are accessible for debugging

Good luck! 🚀
