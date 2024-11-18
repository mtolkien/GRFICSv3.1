# Overview

There are various utility scripts located in the `utils` directory of this project. Each script is designed to perform specific tasks related to data processing and analysis of network attack datasets. Below is a detailed description of each script, including its purpose, functionality, and usage.

## Script 1: Count Attacks

### Purpose:
This script counts the number of attack instances in CSV files within a specified directory. It distinguishes between benign and attack connections based on a specified dataset type (Binary or Multiclass).

### Functionality:
- **Input:** 
  - `directory`: The path to the directory containing the CSV files.
  - `dataset_type`: The type of dataset, either 'Binary' or 'Multiclass'.
  
- **Output:** 
  - Generates a text file (`count_attacks_total.txt`) containing the count of attack rows for each CSV file processed.



## Script 2: Extract Unique Connections with Count

### Purpose:
This script extracts unique connections between source and destination IPs from a given CSV file and counts their occurrences.

### Functionality:
- **Input:**
  - `file_csv`: The path to the input CSV file.
  - `file_txt`: The path to the output text file where unique connections will be saved.
  
- **Output:** 
  - A text file listing each unique connection along with its count.


## Script 3: Merge Files by Category

### Purpose:
This script merges multiple CSV files based on their connection types, sampling a specified number of rows for each category while excluding already sampled data.

### Functionality:
- **Input:**
  - `directory_path`: Directory containing the CSV files to merge.
  - `num_rows_per_category`: Number of rows to sample per connection type.
  - `benign_file_path`: Path to the benign data CSV.
  - `exclude_file_path`: Path to a CSV file containing data to exclude from merging.
  - `output_file`: Path for the output merged CSV.
  
- **Output:** 
  - A merged CSV file containing sampled rows for each connection type.

## Script 4: Count Common Rows

### Purpose:
This script counts the number of common rows between two CSV files.

### Functionality:
- **Input:**
  - `file1`: Path to the first CSV file.
  - `file2`: Path to the second CSV file.
  
- **Output:** 
  - Returns the count of common rows between the two files.


## Script 5: Sample Count


### Purpose:
This script calculates the number of samples to take from various files based on a maximum sample limit across all files.

### Functionality:
- **Input:**
  - `file_path`: The path to the text file containing attack counts per file.
  
- **Output:** 
  - Prints the common number of samples to take for each file and the total sum of samples.

