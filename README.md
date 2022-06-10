log_analyzer.py

Simple command line tool that takes a path to a directory or file, analyzes it and creates a summary json file. 
Without any additional command line options it will create the json in the folder of the script and list the following things:
 - Name of the analyzed file
 - Total amount of bytes transmitted
 - Events per second
 - Most frequent client and destination IP, as list if multiple are equally frequent
 - Least frequent client and destination IP

Command line options:

- -op / --output-path : sets the output path

without any options selected, the json lists all options. You also can select which options it should list:
- -b / --bytes : lists the total amount of bytes transmitted
- -mfip / --most-frequent-ip : lists the most frequent IP, or a list of IPs if multiple are equally frequent
- -lfip / --least-frequent-ip : lists the least frequent IP, or a list of IPs if multiple are equally frequent
- -eps / --events-per-second : lists the events per second