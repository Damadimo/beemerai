# Bug Fix: OpenAI Client Initialization

## Issue
When testing Phase 2, encountered error:
```
Client.__init__() got an unexpected keyword argument 'proxies'
```

## Root Cause
- The code was using `from openai import Client`
- Newer versions of the openai library (1.51.2) use `OpenAI` class instead of `Client`
- The `Client` class in newer versions has a different initialization signature

## Solution
Changed the import and client initialization in `app/boson_api.py`:

**Before:**
```python
from openai import Client

def get_client():
    return Client(api_key=api_key, base_url=base_url)
```

**After:**
```python
from openai import OpenAI

def get_client():
    return OpenAI(api_key=api_key, base_url=base_url)
```

## Testing
To verify the fix works:

```bash
cd ai-car
source .venv/bin/activate  # Activate virtual environment
make run
```

Then:
1. Press Enter to start recording
2. Speak a command
3. Verify the transcript appears without errors

## Notes
- The `OpenAI` class is the standard client in openai >= 1.0.0
- Both `api_key` and `base_url` parameters work correctly with OpenAI class
- No other code changes needed - the API remains the same
