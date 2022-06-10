##log_analyzer.py

Simple command line tool that takes a path to a directory or file, analyzes it and creates a summary json file. 
Without any additional command line options it will create the json in the folder of the script and list the following things:
 - Name of the analyzed file
 - Total amount of bytes transmitted
 - Events per second
 - Most frequent client and destination IP, as list if multiple are equally frequent
 - Least frequent client and destination IP


##Quickstart: 

- Clone or download the repository locally
- Open a terminal window
- cd to the repository
- Run docker-compose up --build -d
- run docker exec -ti log-analyzer_log_analyzer_1 bash
- run python log_analyzer.py [path to directory or file] [additional options]


###In the data directory there is the sample file. to run the script right away the command is: python log_analyzer.py ./data/access.log.gz

##Command line options:

- -op / --output-path : sets the output path

###Without any options selected, the json lists all options. You also can select which options it should list:
- -b / --bytes : lists the total amount of bytes transmitted
- -mfip / --most-frequent-ip : lists the most frequent IP, or a list of IPs if multiple are equally frequent
- -lfip / --least-frequent-ip : lists the least frequent IP, or a list of IPs if multiple are equally frequent
- -eps / --events-per-second : lists the events per second