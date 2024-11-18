"""
This module provides a script for running a set of Python 
files after performing some cleanup operations.

The script first asks the user to select their operating 
system to determine the Python command to use.
It then deletes a set of specific files and all 
files in a results directory.
Finally, it runs a set of Python files.
"""

import os
import subprocess
import shutil
import logging

log_format = '%(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', filemode='a', format=log_format, level=logging.INFO)

def get_python_command():
    """
    Ask the user to select their operating system and 
    return the appropriate Python command.

    Returns:
        str: The Python command ('python' for Windows, 
        'python3' for MacOS/Linux).
    """
    try:
        print("Please select your operating system:")
        print("1. Windows")
        print("2. MacOS / Linux")
        print("3. Exit")

        user_input = input("Enter your choice (1-3): ")
        if user_input == '1':
            return 'python'
        elif user_input == '2':
            return 'python3'
        else:
            exit()
    except Exception as e:
        logging.error(f"Error in get_python_command: {e}")

python_command = get_python_command()

print("""
       .
       |
       |
    ,-'"`-.
  ,'       `.
  |  _____  |      .-( HEY baby,lets go out)
  | (_o_o_) |    ,'    ( and kill all humans.)
  |         | ,-'
  | |HHHHH| |
  | |HHHHH| |
-'`-._____.-'`- 
""")

data_directory = 'data'
code_directory = 'code'

specific_files = [
    'stats.duckdb',
    'stats.duckdb.wal',
    'stats2.duckdb',
    'stats2.duckdb.wal',
    'toolresult.txt',
    'toolresults.txt',
    'dbsize.txt',
    'result.txt',
    'result2.txt',
    'ultimate.duckdb',
    'ultimate.duckdb.wal',
    'test.csv',
    'testresult.txt',
    'testdata.duckdb',
    'testdata.duckdb.wal',
    'etl.duckdb',
    'etl.duckdb.wal'
]

for filename in specific_files:
    try:
        file_path = os.path.join(data_directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed {file_path}")
    except Exception as e:
        logging.error(f"Error in removing file {file_path}: {e}")

results_directory = os.path.join(data_directory, 'results')

if os.path.exists(results_directory):
    for filename in os.listdir(results_directory):
        try:
            file_path = os.path.join(results_directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error(f'Failed to delete {file_path}. Reason: {e}')
    print(f"All files in {results_directory} have been deleted.")
else:
    print(f"The directory {results_directory} does not exist.")

python_files = [
    'etl_step01.py',
    'etl_step02.py',
    'etl_step03.py',
    'etl_step04.py',
    'etl_step05.py',
    'etl_step06.py',
    'etl_step07.py',
    'etl_step08.py',
    'etl_step09.py',
    'etl_step10.py',
    'etl_step11.py',
    'etl_step12.py',
    'etl_step13.py',
    'etl_step14.py',
    'etl_step15.py',
    'etl_step16.py',
    'etl_step17.py',
    'etl_step18.py',
]
 
for python_file in python_files:
    try:
        file_path = os.path.join(code_directory, python_file)
        if os.path.exists(file_path):
            print(f"Running {file_path}")
            subprocess.run([python_command, file_path], check=True)
            print(f"Finished running {file_path}")
    except Exception as e:
        logging.error(f"Error in running {python_file}: {e}")


print("""
                                 ,.   '\'\    ,---.
Quiet, Pinky; I'm pondering.    | \\  l\\l_ //    |   Err ... right,
       _              _         |  \\/ `/  `.|    |   Brain!  Narf!
     /~\\   \        //~\       | Y |   |   ||  Y |
     |  \\   \      //  |       |  \|   |   |\ /  |   /
     [   ||        ||   ]       \   |  o|o  | >  /   /
    ] Y  ||        ||  Y [       \___\_--_ /_/__/
    |  \_|l,------.l|_/  |       /.-\(____) /--.\
    |   >'          `<   |       `--(______)----'
    \  (/~`--____--'~\)  /           U// U / \
     `-_>-__________-<_-'            / \  / /|
         /(_#(__)#_)\               ( .) / / ]
         \___/__\___/                `.`' /   [
          /__`--'__\                  |`-'    |
       /\(__,>-~~ __)                 |       |__
    /\//\\(  `--~~ )                 _l       |--:.
    '\/  <^\      /^>               |  `   (  <   \\
         _\ >-__-< /_             ,-\  ,-~~->. \   `:.___,/
        (___\    /___)           (____/    (____)    `---'
""")
logging.info("ETL Pipeline is done - All your base are belong to us")
print("ETL Pipeline is done - All your base are belong to us")