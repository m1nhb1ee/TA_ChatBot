#!/usr/bin/env python
"""Quick validation script for all critical imports and dependencies."""

import sys
import traceback

def test_imports():
    """Test all critical imports."""
    tests = []
    
    # Test 1: Config
    try:
        import config
        tests.append(("✓ config module", True, None))
    except Exception as e:
        tests.append(("✗ config module", False, str(e)))
        
    # Test 2: Storage utilities
    try:
        from utils.storage import get_metrics, save_chat_session, load_chat_session
        tests.append(("✓ utils.storage", True, None))
    except Exception as e:
        tests.append(("✗ utils.storage", False, str(e)))
    
    # Test 3: Email service
    try:
        from utils.email_service import send_escalation_email
        tests.append(("✓ utils.email_service", True, None))
    except Exception as e:
        tests.append(("✗ utils.email_service", False, str(e)))
    
    # Test 4: Tools
    try:
        from tools.search_materials import search_course_materials
        from tools.code_analyzer import analyze_code_error
        from tools.course_info import get_course_info
        tests.append(("✓ tools modules", True, None))
    except Exception as e:
        tests.append(("✗ tools modules", False, str(e)))
    
    # Test 5: FAISS and RAG
    try:
        from rag.indexer import load_index
        from rag.retriever import retrieve_documents
        tests.append(("✓ rag modules", True, None))
    except Exception as e:
        tests.append(("✗ rag modules", False, str(e)))
    
    # Test 6: LangChain (without OpenAI key, should still import)
    try:
        from langchain_openai import ChatOpenAI
        from langgraph.prebuilt import create_react_agent
        tests.append(("✓ langchain/langgraph", True, None))
    except Exception as e:
        tests.append(("✗ langchain/langgraph", False, str(e)))
    
    # Test 7: Streamlit
    try:
        import streamlit as st
        tests.append(("✓ streamlit", True, None))
    except Exception as e:
        tests.append(("✗ streamlit", False, str(e)))
    
    # Test 8: File paths
    try:
        from pathlib import Path
        paths = {
            "knowledge_base": Path("knowledge_base").exists(),
            "faiss_index": Path("faiss_index").exists(),
            "faiss_index/index.faiss": Path("faiss_index/index.faiss").exists(),
            "knowledge_base/course_info.json": Path("knowledge_base/course_info.json").exists(),
        }
        if all(paths.values()):
            tests.append(("✓ data files", True, None))
        else:
            tests.append(("✗ data files", False, str(paths)))
    except Exception as e:
        tests.append(("✗ data files", False, str(e)))
    
    return tests

if __name__ == "__main__":
    print("=" * 60)
    print("VALIDATION TEST: Checking all imports and dependencies")
    print("=" * 60)
    print()
    
    tests = test_imports()
    passed = 0
    failed = 0
    
    for test_name, success, error in tests:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:<40} [{status}]")
        if error:
            print(f"  Error: {error}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("✓ ALL TESTS PASSED - App is ready for deployment")
        sys.exit(0)
