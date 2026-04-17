# Railway Deployment Execution Plan

## CRITICAL: Before You Start

You MUST have:
1. **Railway Account** - Created at https://railway.app
2. **OPENAI_API_KEY** - From https://platform.openai.com/api-keys
3. **GitHub Account** - Repository already set up and pushed

## Step-by-Step Deployment Instructions

### Phase 1: Authentication & Project Setup

#### Step 1A: Login to Railway
```powershell
cd "c:\Project\Vin AI\Day12\TA_ChatBot"
railway login
```
**Expected**: Browser window opens for authentication. Approve the login request.

---

#### Step 1B: Initialize Railway Project
```powershell
railway init
```
**Expected Output**:
```
? Project name: TA-ChatBot
? Select environment: (create new) → TA-ChatBot
✓ Project created successfully
```

---

### Phase 2: Configuration & Environment

#### Step 2A: Configure Environment Variables
```powershell
railway variables set OPENAI_API_KEY=sk-YOUR_ACTUAL_API_KEY_HERE
railway variables set PYTHONUNBUFFERED=1
railway variables set STREAMLIT_SERVER_HEADLESS=true
railway variables set STREAMLIT_SERVER_ENABLECORS=false
```

**Important**: Replace `sk-YOUR_ACTUAL_API_KEY_HERE` with your actual OpenAI API key.

#### Step 2B: Verify Variables
```powershell
railway variables list
```

**Expected Output**:
```
OPENAI_API_KEY     ••••••••••••••••
PYTHONUNBUFFERED   1
STREAMLIT_SERVER_HEADLESS   true
STREAMLIT_SERVER_ENABLECORS   false
```

---

### Phase 3: Deployment

#### Step 3A: Deploy to Railway
```powershell
railway up --detach
```

**Expected Output**:
```
✓ Deployment initiated
[Project ID: xxxx-xxxx-xxxx]
View your deployment at: https://railway.app/project/xxxx
```

**Duration**: 3-5 minutes for first deployment

---

### Phase 4: Verification & Monitoring

#### Step 4A: Check Deployment Status
```powershell
railway status
```

**Expected Output**:
```
Status: running
Service: ta-chatbot-production
Replicas: 1/1
Last deployed: 2 minutes ago
```

#### Step 4B: View Real-Time Logs
```powershell
railway logs -f
```

**What to look for**:
```
Building image from Dockerfile...
[13:45:12] Running container...
[13:45:25] ✓ Health check passed
[13:45:30] Streamlit running on 0.0.0.0:8501
```

**Wait for**: "Streamlit is running" message

#### Step 4C: Get Your App URL
```powershell
railway open
```
OR
```powershell
railway domains list
```

**Expected**: URL like `https://ta-chatbot-production-xxxx.railway.app`

---

### Phase 5: Post-Deployment Testing

#### Step 5A: Access the Application
```
Navigate to: https://ta-chatbot-production-xxxx.railway.app
(Replace xxxx with your actual domain)
```

#### Step 5B: Test the Chatbot
1. Load the Streamlit interface
2. Try a simple query: "Biến trong C là gì?"
3. Verify the response appears (may take 10-15 seconds for first query)

#### Step 5C: Check Health Endpoint
```bash
curl https://ta-chatbot-production-xxxx.railway.app/_stcore/health
```

**Expected**: 200 OK status

---

## Troubleshooting Guide

### Issue 1: Deployment Stuck at "Building image"
```
❌ ERROR: Build taking too long
```
**Solution**:
- Check network: `ping 8.8.8.8`
- Increase Railway build timeout in dashboard
- Check Docker base image pull: `docker pull python:3.11-slim`

---

### Issue 2: Health Check Failing
```
❌ ERROR: Health check failed 3 times
```
**Cause**: App not starting correctly
**Solution**:
1. View logs: `railway logs -f`
2. Check for OPENAI_API_KEY not set: `railway variables list`
3. Look for import errors in logs
4. Restart service: `railway down && railway up`

---

### Issue 3: OPENAI_API_KEY Not Recognized
```
❌ ERROR: Invalid API key
```
**Solution**:
1. Verify key format: `sk-...` (should start with `sk-`)
2. Test locally first: Create `.env` file with `OPENAI_API_KEY=sk-...`
3. Run locally: `streamlit run app.py`
4. If works locally, re-set on Railway: `railway variables set OPENAI_API_KEY=sk-...`

---

### Issue 4: Port Binding Error
```
❌ ERROR: Address already in use :8501
```
**Solution**:
- Railway automatically assigns port via `$PORT` - should not happen
- Check railway.toml uses `--server.port=$PORT`
- Restart: `railway down && railway up`

---

### Issue 5: FAISS Index Not Loading
```
❌ ERROR: FileNotFoundError: faiss_index/index.faiss
```
**Solution**:
- Verify files committed to git: `git ls-files | grep faiss`
- Check .dockerignore doesn't exclude faiss_index/
- Current `.dockerignore` is correct (doesn't exclude it)

---

## Expected Startup Timeline

| Time | Event | Log Output |
|------|-------|-----------|
| 0s | Build starts | `Building image from Dockerfile...` |
| 90s | Dependencies installed | `Step 5: RUN pip install...` ✓ |
| 120s | Image finished | `exporting to image` ✓ |
| 130s | Container starts | `Running container...` |
| 140s | Port bound | `Streamlit running on 0.0.0.0:8501` |
| 150s | Health check passes | `✓ Health check passed` |
| 160s | READY TO USE | `Streamlit initialized` ✓ |

---

## Final Verification Checklist

- [ ] Railway project created
- [ ] OPENAI_API_KEY set and verified
- [ ] Deployment status: `running`
- [ ] Health check: `passing`
- [ ] App URL accessible
- [ ] Streamlit UI loads
- [ ] Chatbot responds to queries
- [ ] No errors in logs

---

## Next Steps for Persistence

To enable persistent storage (if needed later):

```bash
railway volumes create app_data /app/app_data
```

This would preserve chat history across restarts.

---

## Administrative Commands

```bash
# View all logs from last hour
railway logs --until 1h

# Stop the service
railway down

# Restart the service
railway up

# Remove the project
railway delete

# Pull environment for local development
railway pull
```

---

## Success Indicators

Your deployment is successful when:
1. ✅ `railway status` shows `running`
2. ✅ Logs show no errors
3. ✅ App URL responds with HTTP 200
4. ✅ Streamlit UI loads without errors
5. ✅ Chatbot responds to queries (takes 10-15s first time)

---

## Return to Main Deployment Log

See `deployment_log.md` for the complete deployment timeline and results.
