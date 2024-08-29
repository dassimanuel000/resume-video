
import os


def append_new_line(file_name, text_to_append):
    directory = os.path.dirname(file_name)
    if directory == '':
        directory = '.'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_name, "a+", encoding="utf-8", errors="ignore") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)