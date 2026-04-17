# 🔧 HEALTH CHECK FIX - QUICK DIAGNOSTIC & RESOLUTION

**Issue**: Railway health check failing with "service unavailable"  
**Root Cause**: OPENAI_API_KEY not set on Railway  
**Status**: ✅ FIXED - Code updated with better error handling

---

## ✅ What I Fixed

I've updated the code to handle missing OPENAI_API_KEY gracefully:

### 1. **app.py** - Added API key validation
```python
# Check if OPENAI_API_KEY is set before importing agent
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY is not set. Please configure it on Railway.")
    st.stop()
```

### 2. **config.py** - Added warning messages
```python
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY is not set.")
    print("   Please set the environment variable: OPENAI_API_KEY=sk-...")
```

### 3. **agent.py** - Added error handling for LLM initialization
```python
try:
    if config.OPENAI_API_KEY:
        llm = ChatOpenAI(...)
        agent = create_react_agent(...)
except Exception as e:
    print(f"⚠️  Error initializing LLM/Agent: {e}")
```

### 4. **Dockerfile** - Improved health check timing
- Extended health check start-period from 40s to **60 seconds**
- Added startup script with better logging
- Added diagnostic output showing configuration status

---

## 🚀 REDEPLOYMENT STEPS

### Step 1: Verify OPENAI_API_KEY is set on Railway
```bash
railway variables list
```

**Expected Output**:
```
OPENAI_API_KEY     ••••••••• (should be visible)
```

**If OPENAI_API_KEY is NOT set, do this now**:
```bash
railway variables set OPENAI_API_KEY=sk-YOUR_ACTUAL_API_KEY
```

### Step 2: Redeploy with the fixed code
```bash
# This will pull the latest code from GitHub and rebuild
railway deploy
```

**What Railway will do**:
1. Pull latest code from GitHub (includes all bug fixes)
2. Build new Docker image with improved health checks
3. Start container with extended startup time (60 seconds)
4. Show better error messages if anything fails

### Step 3: Monitor the deployment
```bash
# Watch for the deployment to start
railway status

# View real-time logs
railway logs -f
```

**Good signs** ✅:
```
Starting TA_ChatBot Streamlit Application
Python version: Python 3.11.x
Streamlit version: Streamlit 1.40.0
Starting Streamlit server on port xxxxx
Streamlit is running now...
```

**Bad signs** ❌:
```
⚠️ WARNING: OPENAI_API_KEY environment variable is NOT set
Error initializing LLM/Agent
```
→ **Solution**: Set OPENAI_API_KEY on Railway before redeploying

### Step 4: Verify health check passes
```bash
# Check status
railway status
```

Should show: `running` and health check should pass

---

## 📋 COMPLETE CHECKLIST

Before redeeploy, verify:
- [ ] `railway variables list` shows OPENAI_API_KEY is set
- [ ] OPENAI_API_KEY format is correct (starts with `sk-`)
- [ ] You have a valid OpenAI API key with available credit
- [ ] Git repository has the latest fixes (check GitHub)

For redeploy:
- [ ] Run `railway deploy`
- [ ] Run `railway logs -f` to watch startup
- [ ] Health check passes (status shows `running`)
- [ ] App is accessible at Railway URL

---

## 🔍 WHAT CHANGED IN THE CODE

**3 main files updated**:

1. **app.py** (5 new lines)
   - Imports os module
   - Checks OPENAI_API_KEY before importing agent
   - Displays error and stops if not set

2. **config.py** (5 new lines)
   - Imports sys module
   - Prints warning if OPENAI_API_KEY not set
   - App still starts (graceful degradation)

3. **agent.py** (17 changed lines)
   - Wrapped LLM/agent creation in try-catch
   - Allows app to start even if API key is None
   - Gracefully handles initialization errors

4. **Dockerfile** (15 changed lines)
   - Extended health check start-period to 60s
   - Added startup script with logging
   - Added error details environment variables

**Commit**: `5b57b43`  
**Status**: ✅ Pushed to GitHub

---

## ⏱️ EXPECTED STARTUP TIMELINE (WITH FIXES)

| Time | Event | Log Output |
|------|-------|-----------|
| 0s | Deployment starts | `railway deploy` initiated |
| 15-30s | Build starts | Docker building from Dockerfile |
| 90-120s | Dependencies installing | pip install progress |
| 120-150s | App image ready | Image exporting |
| 150-160s | Container starts | `Running container...` |
| 160-175s | Python initializes | `Starting TA_ChatBot Streamlit Application` |
| 175-190s | Streamlit starts | `Streamlit is running now...` |
| 190-200s | **Health check PASSES** | ✅ Status changes to `running` |

**Total**: ~3-5 minutes from `railway deploy` to fully running

---

## 🆘 IF STILL FAILING AFTER REDEPLOY

### Check 1: Verify OPENAI_API_KEY
```bash
railway variables list
# Should show OPENAI_API_KEY is set (not empty)
```

If not set:
```bash
railway variables set OPENAI_API_KEY=sk-YOUR_KEY
railway deploy
```

### Check 2: View detailed logs
```bash
railway logs -f
# Look for error messages
# Search for "TA_ChatBot" startup message
```

### Check 3: Check container status
```bash
railway status
# Should show "running"
# If shows "crashed", check logs for error
```

### Check 4: Restart if stuck
```bash
railway down          # Stop the service
railway up --detach   # Start it again
railway logs -f       # Watch startup
```

---

## 📞 DEBUGGING COMMANDS

**If health check still fails, try these**:

```bash
# View last 20 lines of logs
railway logs --since 10m

# Check environment variables are set
railway variables list

# Restart deployment
railway down && railway up --detach

# Get detailed status
railway status --verbose

# Check if port is responding
curl -X GET http://localhost/_stcore/health (local test)
```

---

## ✨ WHY THIS FIXES THE ISSUE

**Before**:
1. App imports agent.py
2. agent.py creates LLM with OPENAI_API_KEY=None
3. ChatOpenAI fails/crashes
4. App crashes before Streamlit server starts
5. Health check fails because no server is listening

**After**:
1. app.py checks OPENAI_API_KEY first
2. If missing, displays error and stops gracefully
3. Streamlit server still starts
4. Health check succeeds (server is listening)
5. User sees clear error message about missing API key
6. Once OPENAI_API_KEY is set, chatbot works

---

## 📝 NEXT STEPS

1. **Verify OPENAI_API_KEY on Railway**:
   ```bash
   railway variables list
   ```

2. **If not set, set it now**:
   ```bash
   railway variables set OPENAI_API_KEY=sk-YOUR_KEY
   ```

3. **Redeploy**:
   ```bash
   railway deploy
   ```

4. **Monitor**:
   ```bash
   railway logs -f
   ```

5. **Verify**:
   ```bash
   railway status  # Should say "running"
   railway open    # Open app URL
   ```

---

**Status**: ✅ Code fixed and pushed to GitHub  
**Next Action**: Ensure OPENAI_API_KEY is set, then redeploy  
**Expected Result**: App starts successfully with proper error messages

---

*Last updated: April 17, 2026*
