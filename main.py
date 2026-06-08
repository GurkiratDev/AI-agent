import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
# from google.genai.types import Tool

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from calling_functions import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY") # Getting api key from env

    client = genai.Client(api_key=api_key)
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    verbose_flag = False

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python_file,
            schema_write_file,
        ],
    )

    if len(sys.argv) < 2:
        print("we need a prompt")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[1] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text="prompt")])]

    config = types.GenerateContentConfig(
        temperature=0.1,  # Low temperature makes the model more direct and concise
        system_instruction= system_prompt,
        tools=[available_functions]
    )


    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt,
        config= config
    )

    if response is None or response.usage_metadata is None:
        print("response is None")
        return

    if response.function_calls:
        for function_call_parts in response.function_calls:
            # print(f"Calling function: {function_call_parts.name}({function_call_parts.args})")
            result = call_function(function_call_parts, verbose=verbose_flag)
            print(result.response)
    else:
        print(response.text)


    if verbose_flag is True:
        print(f"prompt token: {response.usage_metadata.prompt_token_count}")
        print(f"response token: {response.usage_metadata.candidates_token_count}")


main()