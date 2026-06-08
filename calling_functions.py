from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import file_content
from functions.run_python_file import run_python
from functions.write_file import write_file

working_directory = "calculator"

def call_function(function_call, verbose: bool = False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    result = ""
    print(function_call.name)
    print(function_call.args)
    if function_call.name == "get_files_info":
        result = get_files_info(working_directory, **function_call.args)

    elif function_call.name == "run_python":
        result = run_python(working_directory, **function_call.args)

    elif function_call.name == "file_content":
        result = file_content(working_directory, **function_call.args)

    elif function_call.name == "write_file":
        result = write_file(working_directory, **function_call.args)

    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call}"},
                )
            ],
        )

    return types.Content(
        role="tool",
         parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
            )
        ],
    )