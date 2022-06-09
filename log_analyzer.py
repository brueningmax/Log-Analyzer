import os, json, argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser(description="print Hello")
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
    help="outputs you the most frequent IP",
    action="store_true"
)

parser.add_argument(
    '-lfip',
    '--least-frequent-ip',
    action="store_true",
    help="outputs you the most frequent IP"
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
    help="outputs the total amount of bytes"
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

def get_most_frequent_IPs(df):
    most_frequent_IP = df['destination_IP'].value_counts()[:1].index.tolist()[0]
    most_frequent_client_IP = df['client_IP'].value_counts()[:1].index.tolist()[0]
    return {'destination_IP': most_frequent_IP, 'client_IP': most_frequent_client_IP}

def get_least_frequent_IPs(df):
    least_frequent_IP = df['destination_IP'].value_counts().index.tolist()[-1]
    least_frequent_client_IP = df['client_IP'].value_counts().index.tolist()[-1]
    return {'destination_IP': least_frequent_IP, 'client_IP': least_frequent_client_IP}

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

for file in file_list:
    file_processed = (os.path.basename(file))
    list_of_lists = []
    index = 0
    bad_lines = {}
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
    output = {'filename': file_processed,}
    if args.bytes:
        output['total_bytes'] = get_total_bytes_transmitted(df)
    if args.events_per_second:
        output['events_per_second'] = get_events_per_second(df)
    if args.most_frequent_ip:
        output['most_frequent_client_IP'] = get_most_frequent_IPs(df)['client_IP']
        output['most_frequent_destination_IP'] = get_most_frequent_IPs(df)['destination_IP']
    if args.least_frequent_ip:
        output['least_frequent_client_IP'] = get_least_frequent_IPs(df)['client_IP']
        output['least_frequent_destination_IP'] = get_least_frequent_IPs(df)['destination_IP']
    if len(bad_lines) > 0:
        output['BAD LINES, PLEASE CHECK'] = bad_lines


    jsonString = json.dumps(output)
    jsonFile = open(f'{args.output_path}{str(file_processed)}_summary.json' if args.output_path else str(
        file_processed) + '_summary.json', "w")
    jsonFile.write(jsonString)
    jsonFile.close()
