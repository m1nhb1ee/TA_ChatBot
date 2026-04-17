import sys
from pathlib import Path

# Test imports
print('Testing backend imports...')
print()

try:
    print('[1] Checking Python version...')
    print(f'    Python {sys.version.split()[0]}')
    
    print('[2] Importing config...')
    import config
    print(f'    * Config loaded')
    print(f'      - Course: {config.COURSE_NAME}')
    print(f'      - Model: {config.LLM_MODEL}')
    has_key = "YES" if config.OPENAI_API_KEY else "NO"
    print(f'      - OpenAI API Key: {has_key}')
    
    print('[3] Checking paths...')
    print(f'    - FAISS Index exists: {config.FAISS_INDEX_DIR.exists()}')
    print(f'    - Knowledge Base exists: {config.KNOWLEDGE_BASE_DIR.exists()}')
    print(f'    - Course Info exists: {config.COURSE_INFO_PATH.exists()}')
    
    print('[4] Testing tool imports...')
    from tools import search_materials
    from tools import code_analyzer  
    from tools import course_info
    print(f'    * All tools importable')
    
    print('[5] Testing RAG imports...')
    from rag import retriever
    print(f'    * RAG retriever importable')
    
    print('[6] Testing agent imports...')
    from agent import core
    print(f'    * Agent core importable')
    
    print('[7] Testing FastAPI app imports...')
    import app
    print(f'    * FastAPI app importable')
    
    print()
    print('SUCCESS: All backend imports verified!')
    
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
