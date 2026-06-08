import os
from google.genai import types

def write_file(working_dir, file_path, content):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not a directory"

    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Error: Could not create directory: {parent_dir} = {e}"


    if not os.path.isfile(abs_file_path):
        pass


    try:
        with open(abs_file_path, "w") as file:
            file.write(content)
            return f"Successfully wrote file to {file_path}"
    except Exception as e:
        return f"Error: Could not write file to {file_path} = {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if it doesn't exits (creates a new required parent dirs safely) relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file which is needed to be write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which should be written as a string",
            ),
        },
    ),
)