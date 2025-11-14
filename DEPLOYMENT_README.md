# 🚀 AI Education Copilot - Deployment Guide

## Overview
Your AI Education Copilot is now ready for deployment! This guide covers deploying both the Flask backend and React frontend to production.

## 📋 Deployment Checklist

### ✅ Completed
- [x] Code pushed to GitHub: https://github.com/LikithGS11/AI-Education-Copilot
- [x] Render configuration files created
- [x] Environment variable support added
- [x] CORS configuration ready

### 🔄 Next Steps
- [ ] Create Render account
- [ ] Deploy backend service
- [ ] Deploy frontend service
- [ ] Configure environment variables
- [ ] Test deployment

---

## 🚀 Deploy to Render (Recommended)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Connect your GitHub repository

### Step 2: Deploy Flask Backend

1. **Create New Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repo: `LikithGS11/AI-Education-Copilot`
   - Select branch: `master`

2. **Configure Service:**
   - **Name:** `ai-copilot-backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `cd flask-ai-copilot && pip install -r requirements.txt`
   - **Start Command:** `cd flask-ai-copilot && python app.py`
   - **Plan:** Free (750 hours/month)

3. **Environment Variables:**
   ```
   FLASK_ENV=production
   PORT=10000
   OPENAI_API_KEY=your_openai_key_here
   GOOGLE_API_KEY=your_google_key_here  # Optional
   GEMINI_API_KEY=your_gemini_key_here  # Optional
   GROQ_API_KEY=your_groq_key_here      # Optional
   ```

4. **Deploy:** Click "Create Web Service"

### Step 3: Deploy React Frontend

1. **Create New Static Site:**
   - Click "New" → "Static Site"
   - Connect your GitHub repo: `LikithGS11/AI-Education-Copilot`
   - Select branch: `master`

2. **Configure Site:**
   - **Name:** `ai-copilot-frontend`
   - **Build Command:** `cd react-ai-copilot && npm install && npm run build`
   - **Publish Directory:** `./react-ai-copilot/dist`
   - **Plan:** Free

3. **Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

4. **Deploy:** Click "Create Static Site"

### Step 4: Update Frontend API URL

After backend deployment, update the frontend's environment variable:
- Replace `your-backend-url` with your actual Render backend URL
- Redeploy the frontend

---

## 🔧 Configuration Files Created

### `flask-ai-copilot/render.yaml`
```yaml
services:
  - type: web
    name: ai-copilot-backend
    runtime: python3
    region: singapore
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 10000
      - key: OPENAI_API_KEY
        sync: false
      - key: GOOGLE_API_KEY
        sync: false
      - key: GEMINI_API_KEY
        sync: false
      - key: GROQ_API_KEY
        sync: false
```

### `react-ai-copilot/vercel.json`
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-url.onrender.com/api/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

---

## 🔑 API Keys Required

You need at least one of these API keys:

### OpenAI (Recommended)
- Get from: https://platform.openai.com/api-keys
- Model: `gpt-4` (paid) or `gpt-3.5-turbo` (cheaper)

### Google Gemini (Free tier available)
- Get from: https://makersuite.google.com/app/apikey
- Model: `gemini-1.5-pro` or `gemini-1.5-flash`

### Groq (Fast inference)
- Get from: https://console.groq.com/keys
- Model: `llama2-70b-4096` or `mixtral-8x7b-32768`

---

## 🧪 Testing Your Deployment

### Backend Tests
```bash
# Health check
curl https://your-backend-url.onrender.com/

# API key check
curl https://your-backend-url.onrender.com/check-keys

# LLM test
curl https://your-backend-url.onrender.com/test-llm
```

### Frontend Tests
1. Open your frontend URL
2. Try generating a module: "Python basics, beginner, 3 days"
3. Verify file explorer shows files
4. Test download functionality

---

## 🚨 Troubleshooting

### Backend Issues
- **Port Error:** Ensure PORT=10000 in environment variables
- **Import Errors:** Check build logs for missing dependencies
- **API Key Issues:** Verify keys are set correctly (case-sensitive)

### Frontend Issues
- **API Connection:** Update VITE_API_URL with correct backend URL
- **Build Errors:** Check if all dependencies are in package.json
- **CORS Issues:** Backend automatically handles CORS

### Common Problems
- **Timeout Errors:** AI generation can take 2-5 minutes
- **Memory Issues:** Free tier has limits, upgrade if needed
- **Rate Limits:** Check your API provider's limits

---

## 💰 Cost Estimation

### Free Tier (Recommended)
- **Backend:** 750 hours/month (~$0)
- **Frontend:** Unlimited static hosting (~$0)
- **AI APIs:** Pay per token usage

### Paid Upgrades (if needed)
- **Render Pro:** $7/month for 100% uptime
- **API Costs:** Varies by provider and usage

---

## 🎯 Production URLs

After deployment, you'll have:
- **Frontend:** `https://ai-copilot-frontend.onrender.com`
- **Backend:** `https://ai-copilot-backend.onrender.com`

Update the frontend's `VITE_API_URL` environment variable with the backend URL.

---

## 📞 Support

If you encounter issues:
1. Check Render deployment logs
2. Verify environment variables
3. Test API endpoints manually
4. Check GitHub repository is public

Your AI Education Copilot is production-ready! 🚀
