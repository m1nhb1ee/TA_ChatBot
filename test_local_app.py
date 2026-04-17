#!/usr/bin/env python3
"""Step 3: Local Application Test - No Unicode Characters"""

import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("STEP 3: LOCAL APPLICATION TEST")
print("="*70)

# Test 1: Module imports
print("\n[3.1] Module Imports Test")
try:
    import streamlit as st
    print("      OK  streamlit")
except ImportError as e:
    print(f"      FAIL streamlit: {e}")
    sys.exit(1)

try:
    import config
    print("      OK  config")
except ImportError as e:
    print(f"      FAIL config: {e}")
    sys.exit(1)

try:
    from langchain_openai import ChatOpenAI
    print("      OK  langchain-openai")
except ImportError as e:
    print(f"      FAIL langchain-openai: {e}")
    sys.exit(1)

try:
    import faiss
    print("      OK  faiss")
except ImportError as e:
    print(f"      FAIL faiss: {e}")
    sys.exit(1)

try:
    from agent import stream_chat
    print("      OK  agent.stream_chat")
except ImportError as e:
    print(f"      FAIL agent.stream_chat: {e}")
    sys.exit(1)

# Test 2: Configuration validation
print("\n[3.2] Configuration Validation")
try:
    print(f"      OK  LLM_MODEL: {config.LLM_MODEL}")
    print(f"      OK  TEMPERATURE: {config.LLM_TEMPERATURE}")
    print(f"      OK  EMBEDDING_MODEL: {config.EMBEDDING_MODEL}")
except Exception as e:
    print(f"      FAIL config: {e}")
    sys.exit(1)

# Test 3: Data files
print("\n[3.3] Data Files Check")
try:
    faiss_path = config.FAISS_INDEX_DIR / "index.faiss"
    if faiss_path.exists():
        size_mb = faiss_path.stat().st_size / (1024*1024)
        print(f"      OK  FAISS: {size_mb:.1f} MB")
    else:
        print(f"      FAIL FAISS not found")
        sys.exit(1)
    
    if config.COURSE_INFO_PATH.exists():
        print(f"      OK  Course Info: {config.COURSE_INFO_PATH}")
    
    slides = list(config.SLIDES_DIR.glob("*.md"))
    print(f"      OK  Slides: {len(slides)} files")
except Exception as e:
    print(f"      FAIL data files: {e}")
    sys.exit(1)

# Test 4: Tools
print("\n[3.4] Tools Loading")
try:
    import tools.search_materials
    print("      OK  search_materials")
    import tools.code_analyzer
    print("      OK  code_analyzer")
    import tools.course_info
    print("      OK  course_info")
except Exception as e:
    print(f"      FAIL tools: {e}")
    sys.exit(1)

# Test 5: Storage
print("\n[3.5] Storage Module")
try:
    from utils.storage import get_metrics, update_metric
    metrics = get_metrics()
    print(f"      OK  Storage: total={metrics.get('total', 0)}")
except Exception as e:
    print(f"      FAIL storage: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("STEP 3 RESULT: ALL LOCAL TESTS PASS")
print("="*70 + "\n")
