import os
from google.genai import types

MAX_CHAR = 10000

def file_content(working_dir, file_path):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not a directory"

    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    file_content_string = ""
    try:
        with open(abs_file_path, 'r') as file:
            file_content_string = file.read(MAX_CHAR)

            if len(file_content_string) > MAX_CHAR:
                file_content_string += f"... File is truncated at 10000 characters"
    except Exception as e:
        return f"Exception reading file: {e} is not a file"

    return file_content_string

schema_get_files_content = types.FunctionDeclaration(
    name="file_content",
    description="Gets the file content as a string in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file relative to the working directory",
            ),
        },
    ),
)