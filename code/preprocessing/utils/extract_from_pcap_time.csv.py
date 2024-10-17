import subprocess
import os

def extract_packets_by_time_range(pcap_file, output_file, start_time, end_time):
    """
    Extracts packets from a pcap file based on the specified time range.

    :param pcap_file: Path to the input pcap file.
    :param output_file: Path to the output filtered pcap file.
    :param start_time: Start time of the range (format: "hh:mm").
    :param end_time: End time of the range (format: "hh:mm").
    """
    if not os.path.exists(pcap_file):
        print(f"Error: file {pcap_file} does not exist.")
        return

    command = [
        "tshark",
        "-r", pcap_file,
        "-w", output_file,
        "-Y", f"frame.time >= \"{start_time}\" && frame.time <= \"{end_time}\""
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Packets extracted and saved in {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing tshark: {e}")

pcap_input = "/path/to/input.pcap"
pcap_output = "/path/to/output.pcap"
start_time = "09:47"
end_time = "10:10"

extract_packets_by_time_range(pcap_input, pcap_output, start_time, end_time)