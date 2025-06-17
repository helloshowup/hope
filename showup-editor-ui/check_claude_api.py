import sys
import os

print("Current Working Directory:", os.getcwd())
print("sys.executable:", sys.executable)
print("sys.path:")
for p in sys.path:
    print(f"  - {p}")

print("\nAttempting to import claude_api...")
try:
    import claude_api
    print("Successfully imported claude_api.")
    print(f"claude_api location: {claude_api.__file__}")
    if hasattr(claude_api, 'Client'):
        print("claude_api.Client exists.")
    else:
        print("claude_api.Client does NOT exist.")
except ImportError as e:
    print(f"Failed to import claude_api: {e}")
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
