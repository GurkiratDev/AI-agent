import os
import subprocess
from google.genai import types

def run_python(working_dir: str, file_path: str, args: []):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not a directory"

    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"

    if not file_path.endswith((".py", ".pyc", ".pyo")):
        return f"Error: {file_path} is not a .py or .pyc file"

    try:
        final_args = ["python", abs_file_path]
        final_args.extend(args)
        output = subprocess.run(final_args, cwd=abs_working_dir, timeout=30, capture_output=True)

        final_output = f"""
        STDOUT: f{output.stdout}
        STDERR: f{output.stderr}
        """

        if output.returncode != 0:
            final_output += f"Process exited with code {output.returncode}\n"
        if final_output != "":
            final_output += "File exited with no output\n"

        return final_output


    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python",
    description="Run the python file in interpreter and also it accepts additional CLI args as an array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file which is needed to run relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as CLI args for the python file",
                items= types.Schema(
                    type = types.Type.STRING
                )
            ),
        },
    ),
)