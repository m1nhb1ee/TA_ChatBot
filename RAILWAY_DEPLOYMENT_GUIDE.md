# TA_ChatBot Railway Deployment Guide

## Project Overview
- **Name**: TA_ChatBot (AI Teaching Assistant for C/C++ Course)
- **Type**: Streamlit Web Application
- **Tech Stack**: Python 3.11, Streamlit, LangChain, OpenAI GPT-4o
- **Repository**: https://github.com/m1nhb1ee/TA_ChatBot
- **Current Status**: Ready for Railway deployment

## Pre-Deployment Checklist

### ✅ Completed
- [x] Dockerfile created (multi-stage, optimized)
- [x] railway.toml configured
- [x] .dockerignore created
- [x] Requirements.txt verified with all dependencies
- [x] Git repository initialized and files committed
- [x] Code pushed to GitHub
- [x] Railway CLI installed (v4.39.0)

### ⚠️ Required Before Deployment
- [ ] Railway account created and authenticated
- [ ] OPENAI_API_KEY obtained from OpenAI dashboard
- [ ] Railway project created
- [ ] Environment variables configured
- [ ] Deployment executed
- [ ] Health checks verified

## Environment Variables Required

The following environment variables must be set on Railway:

```
OPENAI_API_KEY=sk-...              # OpenAI API key (REQUIRED)
PYTHONUNBUFFERED=1                 # Keep Python output unbuffered
STREAMLIT_SERVER_HEADLESS=true     # Enable headless mode
STREAMLIT_SERVER_ENABLECORS=false  # Disable CORS for security
```

## Deployment Steps

### Step 1: Authenticate with Railway
```bash
railway login
# Follow the browser login flow
```

### Step 2: Create Railway Project
```bash
cd c:\Project\Vin AI\Day12\TA_ChatBot
railway init
```

### Step 3: Set Environment Variables
```bash
railway variables set OPENAI_API_KEY=sk-...
railway variables set PYTHONUNBUFFERED=1
```

### Step 4: Deploy to Railway
```bash
railway up --detach
# or use:
railway deploy
```

### Step 5: Monitor Deployment
```bash
railway status
railway logs -f
```

### Step 6: Get App URL
```bash
railway variables get RAILWAY_PRIVATE_URL
railway open
```

## Architecture

### Dockerfile Strategy
- **Stage 1 (Builder)**: Installs Python dependencies
- **Stage 2 (Runtime)**: Minimal production image with non-root user
- **Final Size**: ~241MB content, ~1.09GB disk usage
- **Security**: Non-root user (appuser), read-only where possible
- **Health Checks**: Uses Streamlit health endpoint

### Startup Command
```
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --logger.level=info
```

### Port Configuration
- Default: 8501 (Streamlit standard)
- Railway injects: `$PORT` environment variable
- The app adapts to Railway's assigned port automatically

## Expected Behavior

1. **Build Time**: ~3-5 minutes
2. **Startup Time**: ~30-60 seconds
3. **Health Check**: Will pass after startup initialization
4. **Storage**: App data stored in `/app/app_data/` (ephemeral on Railway)

## Monitoring and Logs

### Check deployment status
```bash
railway status
```

### View real-time logs
```bash
railway logs -f
```

### Common issues and solutions

**Issue**: App crashes during startup
- **Solution**: Check OPENAI_API_KEY is set correctly
- **Check logs**: `railway logs -f`

**Issue**: Health check fails
- **Solution**: Wait 40 seconds for startup, Railway will retry
- **Note**: Configured with 40s start-period in Dockerfile

**Issue**: Port binding error
- **Solution**: Verify Railway is injecting $PORT variable correctly
- **Command**: `railway variables get PORT`

## Cost Considerations

- **Compute**: Minimum tier ($5/month)
- **Memory**: 512MB recommended for FAISS + LangChain
- **Data**: No persistent storage configured (ephemeral)

## Post-Deployment Verification Checklist

- [ ] App is running (railway status)
- [ ] Health check passing
- [ ] Can access app URL
- [ ] Streamlit UI loads
- [ ] Can query the chatbot
- [ ] OPENAI_API_KEY is being used correctly
- [ ] FAISS index loads correctly
- [ ] Knowledge base accessible

## Rollback Plan

If deployment fails:
```bash
railway down
# Fix issues locally
# Test with: streamlit run app.py
# Then redeploy: railway up
```

## Support and Debugging

1. **Check logs**: `railway logs -f` (most important)
2. **Verify env vars**: `railway variables list`
3. **Test locally first**: `streamlit run app.py`
4. **Contact Railway support**: https://railway.app/support

## Additional Resources

- Railway Docs: https://docs.railway.app/
- Streamlit Deployment: https://docs.streamlit.io/deploy
- Environment Setup: Check railway.toml and Dockerfile
