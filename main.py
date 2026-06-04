import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

from functions.get_files_info import get_files_info

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY") # Getting api key from env

    client = genai.Client(api_key=api_key)

    verbose_flag = False

    if len(sys.argv) < 2:
        print("we need a prompt")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[1] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text="prompt")])]

    config = types.GenerateContentConfig(
        max_output_tokens=200,  # Hard limit on response length
        temperature=0.1,  # Low temperature makes the model more direct and concise
        system_instruction="You are a minimalist assistant. Answer in 1-2 short sentences max."
    )

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt,
        config=config
    )
    print(response.text)

    if response is None or response.usage_metadata is None:
        return

    if verbose_flag is True:
        print(f"prompt token: {response.usage_metadata.prompt_token_count}")
        print(f"response token: {response.usage_metadata.candidates_token_count}")


main()