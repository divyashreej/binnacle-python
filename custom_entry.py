import argparse
import sys
import subprocess
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI tool to run selected files")
    parser.add_argument(
        '-v',"--verbose", action='count', default =0, 
        help='increase verbosity -v, -vv,-vvv')
    parser.add_argument('paths', 
                        nargs='+',  # Accepts zero or more positional arguments 
                        help='Names of the test files to run or test directory')
    return parser.parse_args()


def run_files(file_name,env):
    print(f"\n[Running] {file_name}")
    subprocess.run([sys.executable, file_name], env=env, check=True)
    

def run_directory(direc,env):
    for root, _, files in os.walk(direc):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                run_files(full_path,env)


def main():
       
    args =  parse_args()
    
    env = os.environ.copy()
    if args.verbose:
       env["DEBUG"]  = "true" #set env variable
    
    for path in args.paths:
        if os.path.isfile(path) and path.endswith('.py'):
            run_files(path, env) 
        elif os.path.isdir(path):
            run_directory(path, env)
        else:
            print("File or directory does not exist")
