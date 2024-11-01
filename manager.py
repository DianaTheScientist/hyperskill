import os
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')

# put your code here
print('Input the command')


def human_readable_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{round(size_in_bytes)} B"
    elif size_in_bytes < 1024 ** 2:
        return f"{round(size_in_bytes / 1024)} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{round(size_in_bytes / (1024 ** 2))} MB"
    else:
        return f"{round(size_in_bytes / (1024 ** 3))} GB"


while True:
    user_input = input().strip()
    try:
        if user_input == 'quit':
            break

        elif user_input == 'pwd':
            print(os.getcwd())
            pass

        elif user_input.startswith('cd '):
            path = user_input[3:].strip()
            try:
                if path == '..':
                    os.chdir('..')
                else:
                    os.chdir(path)
                print(os.getcwd())
            except FileNotFoundError:
                print("Error: Directory does not exist")

        elif user_input in ['ls', 'ls -l', 'ls -lh']:
            directories = []
            files = []
            for item in os.listdir():
                if os.path.isdir(item):
                    directories.append(item)
                else:
                    files.append(item)
            for directory in directories:
                print(directory)

            if user_input == 'ls':
                for file in files:
                    print(file)

            elif user_input == 'ls -l':
                for file in files:
                    size = os.stat(file).st_size
                    print(f'{file} {size}')

            elif user_input == 'ls -lh':
                for file in files:
                    size = os.path.getsize(file)
                    readable_size = human_readable_size(size)
                    print(f'{file} {readable_size}')
            else:
                os.chdir(path)
                print('Invalid command')

        elif user_input.startswith('rm'):
            command_parts = user_input.split()
            if len(command_parts) != 2:
                print('Specify the file or directory')
            else:
                _, file_extension = command_parts
                files_to_delete = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(file_extension)]
                if not files_to_delete:
                    print(f'File extension {file_extension} not found in this directory')
                if '.' not in user_input:
                    print("No such file or directory")
                else:

                    try:
                        for filename in os.listdir():
                            if os.path.isfile(filename) and filename.endswith(file_extension):
                                os.remove(filename)
                    except FileNotFoundError:
                        print(f"File extension {file_extension} not found in this directory")

        elif user_input.startswith('mv'):
            command_parts = user_input.split()
            if user_input == 'mv':
                print('Specify the current name of the file or directory and the new location and/or name')
            else:
                if len(command_parts) != 3:
                    print('Specify the current name of the file or directory and the new location and/or name')
                else:
                    _, source, destination = command_parts
                    if not source.startswith('.'):
                        if not os.path.exists(source):
                            print("No such file or directory")
                        files_to_move = [source]
                    else:
                        file_extension = source if source.startswith('.') else '.' + source
                        files_to_move = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(file_extension)]
                        if not files_to_move:
                            print(f"File extension {file_extension} not found in this directory")

                    for filename in files_to_move:
                        source_path = filename

                        if os.path.exists(destination) and os.path.isdir(destination):
                            destination_path = os.path.join(destination, filename)

                            if os.path.exists(destination_path):
                                while True:
                                    replace = input(
                                        f"{filename} already exists in this directory. Replace? (y/n) ").strip().lower()
                                    if replace == 'y':
                                        shutil.move(source_path, destination_path)
                                        print(f"Replaced {filename}")
                                        break
                                    elif replace == 'n':
                                        print(f"Skipped {filename}")
                                        break
                                    else:
                                        print("Please enter 'y' or 'n'")
                            else:
                                shutil.move(source_path, destination_path)
                                print(f"Moved {filename} to {destination}")

                        else:
                            destination_path = destination
                            if os.path.exists(destination_path):
                                print("The file or directory already exists")
                            else:
                                shutil.move(source_path, destination_path)
                                print(f"Moved {filename} to {destination}")

        elif user_input.startswith('mkdir'):
            directory_name = user_input[5:].strip()
            if not directory_name:
                print('Specify the name of the directory to be made')
            else:
                try:
                    os.mkdir(user_input[6:])
                except FileExistsError:
                    print('The directory already exists')

        elif user_input.startswith('cp'):
            command_parts = user_input.split()
            if user_input == 'cp':
                print('Specify the file')
            else:
                if len(command_parts) != 3:
                    print('Specify the current name of the file or directory and the new location and/or name')
                else:
                    _, source, destination = command_parts
                    if '.' in source and not source.startswith('.'):
                        if os.path.isfile(source):
                            files_to_copy = [source]
                        else:
                            print(f"No such file or directory")
                    files_to_copy = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(source)]
                    if not files_to_copy:
                        print(f"File extension {source} not found in this directory")
                    else:
                        if not os.path.isdir(destination):
                            print("Destination directory does not exist")
                        else:
                            for filename in files_to_copy:
                                source_path = filename
                                destination_path = os.path.join(destination, filename)
                                if os.path.exists(destination_path):
                                    replace = input(f"{filename} already exists in this directory. Replace? (y/n) ")
                                    if replace.lower() != 'y':
                                        continue
                                shutil.copyfile(source_path, destination_path)

    except FileNotFoundError:
        print("Error: Directory does not exist")
