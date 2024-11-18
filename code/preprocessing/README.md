# Overview

This directory contains five Python scripts designed to facilitate preprocessing of network traffic data for analysis. Each script serves a specific purpose in cleaning, transforming, and organizing data from various sources. Below is a detailed description of each script and its functionality.

## Script 1: Add Connection Column

This script processes CSV files containing network connection data, adds a column indicating the type of connection, and categorizes potential attacks based on the directory structure and file names.

### Key Functions:
- **load_unique_connections(txt_file)**: Reads a text file containing unique connections and returns a set of these connections.
- **determine_attack_category(filename, directory_path)**: Determines the category of an attack based on the file name and directory path.
- **add_connection_column(df, unique_connections, attack_category, process_type)**: Adds a column to the DataFrame to label each connection as either benign or an attack based on the unique connections.
- **process_directory(input_directory_path, output_directory_path, txt_unique_connections, process_type)**: Walks through the specified input directory, processes each CSV file, and saves the modified DataFrame to an output directory.


## Script 2: Clean CSV

This script cleans CSV files by handling missing values, ensuring proper data types, and removing rows with critical missing information.

### Key Functions:
- **clean_csv(input_directory_path, output_directory_path)**: Iterates over CSV files in the input directory, cleans the data by filling missing values and converting data types, then saves the cleaned data to the output directory.



## Script 3: Conversion to CSV

This script processes PCAP files using `tshark`, converts them into CSV format, and modifies the headers and protocol mappings.

### Key Functions:
- **map_protocol_to_number(protocol)**: Maps protocol names to integers for easier analysis.
- **preprocess_frame_time_delta(df)**: Computes packet frequency based on the frame time delta.
- **process_pcapng(input_file, output_file, extract_sample, max_lines)**: Calls `tshark` to extract relevant fields from PCAP files and saves the results to a CSV file.
- **rename_and_modify_csv(output_file, custom_labels)**: Modifies the CSV headers and applies protocol mapping.



## Script 4: Merge Binary Files

This script merges multiple CSV files containing binary connection data, filtering for specific connection types and ensuring a balanced dataset by sampling benign connections.

### Key Functions:
- **get_filtered_rows(file_path, rows_per_file, chunk_size)**: Retrieves filtered rows from a CSV file based on connection type.
- **merge_files(directory_path, num_rows, benign_file_path, output_file, chunk_size)**: Merges attack data from various files while matching the number of benign rows to create a balanced dataset.


## Script 5: Merge Multiclass Files

This script samples rows from multiple CSV files based on different connection categories, ensuring each category is represented in the final output.

### Key Functions:
- **get_file_categories(file_path, chunk_size)**: Extracts unique connection categories from a CSV file.
- **process_category(file_path, category, num_rows_per_category, chunk_size)**: Samples rows for a specific connection category.
- **merge_files(directory_path, num_rows_per_category, benign_file_path, output_file, num_attack_categories, chunk_size)**: Merges sampled rows from multiple files, ensuring a balanced representation of attack categories and benign connections.

