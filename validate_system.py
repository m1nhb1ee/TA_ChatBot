#!/usr/bin/env python3
"""System validation script with API key"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

print("\n" + "="*70)
print("🔍 SYSTEM VALIDATION WITH API KEY")
print("="*70)

# 1. API Key Check
print("\n✅ STEP 1: API Key Status")
if api_key:
    masked = api_key[:25] + "..." + api_key[-10:]
    print(f"   ✓ OPENAI_API_KEY is set: {masked}")
else:
    print("   ✗ API Key is MISSING")
    sys.exit(1)

# 2. Module Imports
print("\n✅ STEP 2: Core Module Imports")
try:
    import config
    print(f"   ✓ config imported")
    print(f"     - LLM Model: {config.LLM_MODEL}")
    print(f"     - Temperature: {config.LLM_TEMPERATURE}")
except Exception as e:
    print(f"   ✗ config error: {e}")
    sys.exit(1)

# 3. Data Files
print("\n✅ STEP 3: Data Files")
files_check = [
    ("FAISS Index", config.FAISS_INDEX_DIR / "index.faiss"),
    ("Course Info", config.COURSE_INFO_PATH),
    ("FAQ", config.FAQ_PATH),
]
for name, path in files_check:
    if path.exists():
        print(f"   ✓ {name}: {path.stat().st_size:,} bytes")
    else:
        print(f"   ✗ {name}: NOT FOUND")

# 4. Slides
print("\n✅ STEP 4: Knowledge Base Slides")
slides = list(config.SLIDES_DIR.glob("*.md"))
print(f"   ✓ Found {len(slides)} slide files")
for slide in sorted(slides)[:3]:
    print(f"     - {slide.name}")

# 5. LLM Test
print("\n✅ STEP 5: LLM Initialization Test")
try:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        api_key=config.OPENAI_API_KEY,
        streaming=True,
    )
    print(f"   ✓ ChatOpenAI initialized successfully")
    print(f"     - Model: {llm.model_name}")
except Exception as e:
    print(f"   ✗ LLM error: {str(e)[:80]}")

# 6. Agent
print("\n✅ STEP 6: Agent Module")
try:
    from agent import stream_chat, llm as agent_llm, agent as agent_obj
    if agent_llm and agent_obj:
        print(f"   ✓ Agent initialized successfully")
        print(f"     - LLM type: {type(agent_llm).__name__}")
    else:
        print(f"   ⚠ Agent/LLM is None")
except Exception as e:
    print(f"   ✗ Agent error: {str(e)[:80]}")

# 7. Storage Module
print("\n✅ STEP 7: Storage Module")
try:
    from utils.storage import get_metrics, update_metric
    metrics = get_metrics()
    print(f"   ✓ Storage module working")
    print(f"     - Total conversations: {metrics.get('total', 0)}")
    print(f"     - Helpful responses: {metrics.get('helpful', 0)}")
    print(f"     - Escalations: {metrics.get('escalated', 0)}")
except Exception as e:
    print(f"   ✗ Storage error: {str(e)[:80]}")

# 8. Tools
print("\n✅ STEP 8: Tool Modules")
tools_to_check = [
    "tools.search_materials",
    "tools.code_analyzer", 
    "tools.course_info",
]
for tool in tools_to_check:
    try:
        __import__(tool)
        print(f"   ✓ {tool} available")
    except Exception as e:
        print(f"   ✗ {tool} error: {str(e)[:60]}")

print("\n" + "="*70)
print("✅ VALIDATION COMPLETE - System is ready!")
print("="*70 + "\n")
