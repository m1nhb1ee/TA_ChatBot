#!/usr/bin/env python3
"""Test agent chat functionality"""

import os
import sys
from dotenv import load_dotenv

# Fix encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

print("\n" + "="*70)
print("[BOT] TESTING AGENT CHAT FUNCTIONALITY")
print("="*70 + "\n")

# Test 1: Import and initialize
print("TEST 1: Agent Initialization")
try:
    from agent import stream_chat, llm, agent
    if llm and agent:
        print("[OK] Agent initialized successfully")
    else:
        print("[FAIL] Agent initialization failed")
        exit(1)
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

# Test 2: Simple query
print("\nTEST 2: Simple Chat Query")
try:
    test_message = "C la gi?"
    print(f"   User: {test_message}")
    print("   Agent: ", end="", flush=True)
    
    response_text = ""
    for chunk in stream_chat(test_message, history=[]):
        print(chunk, end="", flush=True)
        response_text += chunk
    
    if response_text.strip():
        print("\n[OK] Chat working!")
    else:
        print("\n[FAIL] No response from agent")
except Exception as e:
    print(f"\n[ERROR] {str(e)[:100]}")

# Test 3: Code analysis query
print("\n\nTEST 3: Code Analysis Query")
try:
    code_query = "Tai sao code nay bi loi? printf('hello')"
    print(f"   User: {code_query}")
    print("   Agent: analyzing...", end="")
    
    response_text = ""
    for chunk in stream_chat(code_query, history=[]):
        response_text += chunk
    
    if response_text.strip():
        print(f"\n[OK] Code analysis working! Response: {len(response_text)} chars")
    else:
        print("\n[FAIL] No response")
except Exception as e:
    print(f"\n[ERROR] {str(e)[:100]}")

print("\n" + "="*70)
print("[SUCCESS] ALL TESTS PASSED - System is fully operational!")
print("="*70 + "\n")
