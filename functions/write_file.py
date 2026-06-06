import os

MAX_CHAR = 10000

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