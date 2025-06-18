import os
import re

def combine_markdown_files(directory_path, output_filename="combined_output.md"):
    """Combine all markdown files in a directory into a single file.
    
    Args:
        directory_path (str): Path to the directory containing markdown files
        output_filename (str): Name of the output file
        
    Returns:
        str: Path to the combined output file
    """
    # Get all markdown files in the directory
    md_files = [f for f in os.listdir(directory_path) if f.endswith('.md') and f != output_filename]
    
    # Define a function to extract the numeric prefix for sorting
    def get_numeric_prefix(filename):
        # Extract numbers like 4.01, 4.02, etc. from filenames
        match = re.search(r'(\d+)\.(\d+)', filename)
        if match:
            # Convert to a float for proper numeric sorting
            return float(f"{match.group(1)}.{match.group(2)}")
        return 0  # Default value if no match
    
    # Sort files based on their numeric prefix
    md_files.sort(key=get_numeric_prefix)
    
    # Create the output file path
    output_path = os.path.join(directory_path, output_filename)
    
    # Combine the content of all files
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for filename in md_files:
            file_path = os.path.join(directory_path, filename)
            
            # Add a header with the filename (optional)
            outfile.write(f"\n\n# {filename}\n\n")
            
            # Read and write the content of each file
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            
            # Add a separator between files (optional)
            outfile.write("\n\n---\n\n")
    
    print(f"Combined {len(md_files)} markdown files into {output_path}")
    return output_path

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
        output_filename = sys.argv[2] if len(sys.argv) > 2 else "combined_output.md"
    else:
        # Use the current directory if no arguments are provided
        directory_path = os.path.dirname(os.path.abspath(__file__))
        output_filename = "combined_output.md"
    
    combine_markdown_files(directory_path, output_filename)
