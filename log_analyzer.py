import os, json, argparse, gzip
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Simple command line tool that takes the path to a file or directory and analyzes the log to create a json listing the total bytes transmitted, events per secont, most and least frequent client and destination ID. By default all options are listed.")
parser.add_argument('path', type=Path)

parser.add_argument(
    '-op',
    '--output-path',
    type=Path,
    help="enter the save location of the json"
)

parser.add_argument(
    '-mfip',
    '--most-frequent-ip',
    action="store_true",
    help="lists the most frequent IPs"
)

parser.add_argument(
    '-lfip',
    '--least-frequent-ip',
    action="store_true",
    help="lists the least frequent IP"
)

parser.add_argument(
    '-eps',
    '--events-per-second',
    action="store_true",
    help="lists the events per second"
)

parser.add_argument(
    '-b',
    '--bytes',
    action="store_true",
    help="lists the total amount of bytes"
)


def define_dataframe(list):
    df_columns = ['timestamp', 'response_size', 'client_IP', 'HTTP_code', 'Resp_size', 'HTTP_method', 'URL',
                  'username', 'destination_IP', 'Resp_type']
    df = pd.DataFrame(list, columns=df_columns)
    return df


def get_total_bytes_transmitted(df):
    df['response_size'] = pd.to_numeric(df['response_size'])
    df['Resp_size'] = pd.to_numeric(df['Resp_size'])
    total_bytes = df['Resp_size'].sum() + df['response_size'].sum()
    return int(total_bytes)


def get_events_per_second(df):
    df['timestamp'] = pd.to_numeric(df['timestamp'])
    df = df.sort_values(by=['timestamp'])
    start_time = df['timestamp'].iloc[0]
    end_time = df['timestamp'].iloc[-1]
    timeframe = end_time - start_time
    count_row = df.shape[0]
    return float(count_row / timeframe)


# ASSUMPTION: Preferred behavior is returning most frequent IPs in a list so if multiple repeat the same amount of time, all will be listed
def get_most_frequent_IPs(df):
    most_frequent_IP = df['destination_IP'].mode().tolist()
    most_frequent_client_IP = df['client_IP'].mode().tolist()
    return {'destination_IP': most_frequent_IP, 'client_IP': most_frequent_client_IP}

# ASSUMPTION: Preferred behavior is returning most frequent IPs in a list so if multiple repeat the same amount of time, all will be listed
def get_least_frequent_IPs(df):
    max = df['client_IP'].value_counts()
    least_client_IPs = []
    for index, value in max.items():
        if value == 1:
            least_client_IPs.append(index)
    max = df['client_IP'].value_counts()
    least_desti_IPs = []
    for index, value in max.items():
        if value == 1:
            least_desti_IPs.append(index)
    return {'destination_IP': least_desti_IPs, 'client_IP': least_client_IPs}

args = parser.parse_args()
file_list = []
if os.path.isdir(args.path):
    for file in os.listdir(args.path):
        name, extension = os.path.splitext(file)
        if extension in ['.txt', '.log']:
            file_list.append(os.path.abspath(f'{args.path}\{file}'))

elif os.path.isfile(args.path):
    file_list.append(args.path)

# check if any options are used, if not set all to True
if not any([args.most_frequent_ip, args.least_frequent_ip, args.events_per_second, args.bytes]):
    args.most_frequent_ip = args.least_frequent_ip = args.events_per_second = args.bytes = True

if len(file_list) == 0:
    print('Entered file path is not valid or does not contain valid files.')
else:
# ASSUMPTION: when providing a directory path, we should create a file per input file
    for file in file_list:
        file_processed = (os.path.basename(file))
        list_of_lists = []
        index = 0
        bad_lines = {}
        name, extension = os.path.splitext(file)
        if extension in ['.gz']:
            a_file = gzip.open(file, 'rt', encoding="utf8")
        else:
            a_file = open(file, 'r', encoding="utf8")

        for line in a_file:
            index += 1
            stripped_line = line.strip()
            line_list = stripped_line.split()

            if len(line_list) == 10:
                list_of_lists.append(line_list)

            elif len(line_list) != 0:
                bad_lines[f'Line {index}'] = line_list
        a_file.close()

        df = define_dataframe(list_of_lists)
        output = {'filename': file_processed, }

        if args.bytes:
            output['total_bytes'] = get_total_bytes_transmitted(df)
        if args.events_per_second:
            output['events_per_second'] = get_events_per_second(df)

# ASSUMPTION: for IPs we want to list both client and destination IPs
        if args.most_frequent_ip:
            most_frequent = get_most_frequent_IPs(df)
            output['most_frequent_client_IP'] = most_frequent['client_IP']
            output['most_frequent_destination_IP'] = most_frequent['destination_IP']
        if args.least_frequent_ip:
            least_frequent = get_least_frequent_IPs(df)
            output['least_frequent_client_IP'] = least_frequent['client_IP']
            output['least_frequent_destination_IP'] = least_frequent['destination_IP']

        if len(bad_lines) > 0:
            output['BAD LINES, PLEASE CHECK'] = bad_lines
            print('BAD LINES ENCOUNTERED, PLEASE CHECK OUTPUT JSON')

# Creating the JSON
        jsonString = json.dumps(output)
        jsonFile = open(f'{args.output_path}{str(file_processed)}_summary.json' if args.output_path else str(
            file_processed) + '_summary.json', "w")
        jsonFile.write(jsonString)
        jsonFile.close()
