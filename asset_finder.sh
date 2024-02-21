#!/bin/bash

# Banner

echo   ██████╗ ██████╗  █████╗ ████████╗███████╗██████╗ 
echo  ██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
echo  ██║  ███╗██████╔╝███████║   ██║   █████╗  ██████╔╝
echo  ██║   ██║██╔══██╗██╔══██║   ██║   ██╔══╝  ██╔══██╗
echo  ╚██████╔╝██║  ██║██║  ██║   ██║   ███████╗██║  ██║
echo   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

echo "Usage ./asset_finder.sh -F <filename> -f <subdomain>"

# Command line parameters

PARAM=$1
FILENAME=$2

# Create output file for Subdomain discovery 
if [ ! -f "subfinder_output.txt" ]; 
	then 
		touch "subfinder_output.txt"
	fi

# Check for each subdomain in the file
if [ "$PARAM" == "-F" ];
	then

	while IFS= read -r line; 
	do 
		subfinder -d $line >> subfinder_output.txt 
	done < "$FILENAME"

# Check for a single subdomain
elif [ "$PARAM" == "-f" ]; 
	then
		subfinder -d $FILENAME >> subfinder_output.txt
fi

# Port discovery
naabu -l subfinder_output.txt -o naabu_output.txt

# Domain probing
cat naabu_output.txt | ~/go/bin/httpx -location -fr -sc -ports 80,443,8080,8443 -fc 404 -o httpx_output.txt


# Asset discovery
#subfinder -d account.api.here.com > subdomains.txt
#subfinder -d account.here.com >> subdomains.txt
#subfinder -d mobilitygraph.hereapi.com >> subdomains.txt

# Information gathering
#naabu -l subdomains.txt -o open_ports.txt

# Content discovery
#cat subdomains.txt | ~/go/bin/httpx -location -fr -sc -ports 80,443,8080,8443 -fc 404 -o responses.txt