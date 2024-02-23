import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-dut', default=None, help='enter the option for ls command')
parser.add_argument('-base_file', default=None, help='enter the option for ls command')
args = parser.parse_args()
modified_file_name = args.dut + ".sv"
file_to_modify = args.base_file
print(modified_file_name)
source_directory = "/Users/mac/project1/chip/list"
destination_directory = "/Users/mac/project/chip/dv/top_tb"
specified_duts = [args.dut]

source_file_path = os.path.join(source_directory, file_to_modify)
destination_file_path = os.path.join(destination_directory, modified_file_name)

try:
    if os.path.exists(source_file_path):
        with (open(os.path.join(source_directory, file_to_modify), "r") as file):
            lines = file.readlines()
            axi_dut_lines = [line.strip() for line in lines if args.dut in line]
        if axi_dut_lines:
            shutil.copy2(source_file_path, destination_directory)
            try:
                with (open(os.path.join(destination_directory, file_to_modify), "r") as file):
                    lines = file.readlines()
                axi_dut_lines = [line.strip() for line in lines if args.dut in line]

                if axi_dut_lines:
                    for i, line in enumerate(lines):
                        if '_DUT' in line and args.dut not in line:
                            lines[i] = f'# {line}'
                            with open(os.path.join(destination_directory, file_to_modify), "w") as file:
                                file.write(''.join(lines))
                else:
                    print(f"No line containing {args.dut} found in the file.")
            except (FileNotFoundError, OSError) as e:
                print(f"An error occurred: {e}")
                raise
            os.rename(os.path.join(destination_directory, file_to_modify), destination_file_path)
            print("File copied, modified, and renamed successfully!")
        else:
            print(f"No line containing {args.dut} found in the file.")
    else:
        print(f"Error: {file_to_modify} not found in source directory.")
except (FileNotFoundError, OSError) as e:
    print(f"An error occurred: {e}")
