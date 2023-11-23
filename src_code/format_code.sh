#!/bin/bash

# Define the destination directory as 'src_code_formatted' inside the current working directory
DEST_DIR="./src_code_formatted"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Traverse all Java files in the current directory (which will be 'src_code/tmp')
find . -type f -name "*.java" | while read -r file; do
    # Remove the leading './' from the file path
    file="${file:2}"
    
    # Convert directory separators to dots, and prepend the package path
    dest_filename=$(echo "$file" | tr '/' '.')

    # Copy the Java file to the destination directory with the modified name
    cp "$file" "$DEST_DIR/$dest_filename"
done

