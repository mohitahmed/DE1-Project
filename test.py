import os
import csv
import hdf5_getters

def load_h5_files_recursive(directory):
    """
    Recursively load all HDF5 files (.h5) in the specified directory and its subdirectories.
    
    Args:
    - directory: Path to the directory containing HDF5 files.
    
    Returns:
    - List of opened HDF5 file objects.
    """
    h5_files = []
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".h5"):
                filepath = os.path.join(root, filename)
                h5_file = hdf5_getters.open_h5_file_read(filepath)
                h5_files.append((h5_file, filepath))  # Also store filepath for reference
    return h5_files

def extract_artist_names(h5_files):
    """
    Extract artist names from the opened HDF5 files.
    
    Args:
    - h5_files: List of opened HDF5 file objects.
    
    Returns:
    - List of tuples (filepath, artist_name) containing extracted information.
    """
    extracted_info = []
    for h5_file, filepath in h5_files:
        try:
            artist_name_bytes = hdf5_getters.get_artist_name(h5_file)
            artist_name = artist_name_bytes.decode('utf-8')
            track_id_bytes = hdf5_getters.get_track_id(h5_file)
            track_id = track_id_bytes.decode('utf-8')
            title_bytes = hdf5_getters.get_title(h5_file)
            title = title_bytes.decode('utf-8')
            extracted_info.append((track_id, artist_name, title))
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
        finally:
            # Don't forget to close each file after you're done with it
            h5_file.close()
    return extracted_info

def save_to_csv(data, output_file):
    """
    Save the extracted information to a CSV file.
    
    Args:
    - data: List of tuples (filepath, artist_name) containing extracted information.
    - output_file: Path to the output CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Track Id", "Artist","Title"])  # Write header
        csv_writer.writerows(data)  # Write data rows

# Directory containing HDF5 files
directory = r"C:\Users\mhtah\Downloads\millionsongsubset\MillionSongSubset\A"

# Load all HDF5 files in the directory and its subdirectories
h5_files = load_h5_files_recursive(directory)

# Extract artist names from the HDF5 files
extracted_info = extract_artist_names(h5_files)

# Path to the output CSV file
output_csv_file = "extracted_info.csv"

# Save extracted information to CSV file
save_to_csv(extracted_info, output_csv_file)

print("Information saved to:", output_csv_file)
