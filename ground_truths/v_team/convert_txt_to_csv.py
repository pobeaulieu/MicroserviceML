import os
import csv

def process_text_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)

        current_separator = None
        lines = []
        for line in input_file:
            line = line.strip()
            if line.startswith(('MS', 'AS')):
                if lines:
                    csv_writer.writerow(lines)
                current_separator = line
                lines = []
            else:
                lines.append(line)

        if lines:
            csv_writer.writerow(lines)

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(root, f'{os.path.splitext(file)[0]}.csv')
                process_text_file(input_file_path, output_file_path)
                print(f'Processed: {input_file_path}')

# Replace 'your_folder_path' with the path to the folder containing text files
folder_path = os.path.dirname(os.path.realpath(__file__))
process_folder(folder_path)
