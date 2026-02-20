import requests
import json
import random
import time

# Load tokens into a list
with open("tokens.txt", "r") as f:
    tokens = [line.strip() for line in f.readlines()]

# Load messages
with open("messages.txt", "r") as f:
    all_messages = [line.strip() for line in f.readlines()]

channel_id = input("Channel ID: ")
# We don't need 'amount' anymore if we want to use every token exactly once
# But we can use it to limit the run if the list is huge.

url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

def get_nonce():
    return str(random.randint(10**18, 10**19))

def send_request():
    if not tokens:
        print("Finished: No more tokens left to use.")
        return "empty"

    # .pop(0) takes the FIRST token and removes it from the list
    # This ensures it can NEVER be picked again during this session
    current_token = tokens.pop(0)
    current_message = random.choice(all_messages)

    headers = {
        "Authorization": current_token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"
    }

    data = {
        "content": current_message,
        "nonce": get_nonce(),
        "tts": False
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"Token used successfully. Remaining tokens: {len(tokens)}")
        elif response.status_code == 401:
            print(f"Token was unauthorized. Already removed from active session.")
            # Since we already popped it, we just update the file
            with open("tokens.txt", "w") as f:
                f.write("\n".join(tokens))
        else:
            print(f"Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # This loop runs until the tokens list is empty
    while tokens:
        result = send_request()
        if result == "empty":
            break
