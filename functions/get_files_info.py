import os

def get_files_info(working_dir, directory='.'):
    abs_working_dir = os.path.abspath(working_dir)
    abs_directory = os.path.abspath(os.path.join(working_dir,directory))
    if not abs_directory.startswith(abs_working_dir):
        return f"Error: {directory} is not a directory"

    final_response = ""
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)

        final_response += f"{content}: file size: {size} bytes, is directory:{is_dir}\n"

    return final_response