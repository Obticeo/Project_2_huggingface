import itertools
import time

import os
# from dotenv import load_dotenv
# load_dotenv()

# Load API keys from Render environment variables
API_KEYS = [
    {"key": os.environ.get("API_KEY_1"), "req_timestamps": []},
    {"key": os.environ.get("API_KEY_2"), "req_timestamps": []},
    {"key": os.environ.get("API_KEY_3"), "req_timestamps": []},
]

# Example usage
for api in API_KEYS:
    print("Loaded API key")


key_cycle = itertools.cycle(API_KEYS)
MAX_REQS_PER_MIN = 5


def cleanup_usage(key_info):
    """Remove requests older than 60s."""
    now = time.time()
    key_info["req_timestamps"] = [t for t in key_info["req_timestamps"] if now - t < 60]


def get_api_key(auto_wait=True):
    """Return an API key that has quota. Waits if needed."""
    while True:
        for _ in range(len(API_KEYS)):
            key_info = next(key_cycle)
            cleanup_usage(key_info)

            if len(key_info["req_timestamps"]) < MAX_REQS_PER_MIN:
                key_info["req_timestamps"].append(time.time())
                return key_info["key"]

        if auto_wait:
            # Find soonest timestamp that will expire
            next_free_time = min(
                min(k["req_timestamps"]) for k in API_KEYS if k["req_timestamps"]
            )
            sleep_for = max(0, 60 - (time.time() - next_free_time))
            print(f"⏳ All keys exhausted. Waiting {sleep_for:.1f}s...")
            time.sleep(sleep_for + 0.1)
        else:
            raise RuntimeError("🚨 All API keys hit 5 req/min limit")
