#R.I.P Checker - Requested IP Checker v1.0.0

from http.client import responses
import re
from urllib import response
from aiohttp import request
import requests
from bs4 import BeautifulSoup
from colorama import Fore
import os
import json

#Static data
ip_services = {
            1:"https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data&ip=",
            2:"https://www.ipaddressguide.com//ip-geolocation"
}

generic_response_structure = {"coordinates": {"latitude": "0.0","longitude": "0.0"},
                            "ip": "", 
                            "isp": "", 
                            "host": {"ip_address": ""}, 
                            "status": False, 
                            "country": "", 
                            "region": "", 
                            "city": "", 
                            "location": "", 
                            "area_code": "", 
                            "country_code": ""
}

generic_header_data = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1",
        "Te": "trailers",
        "Connection": "close"
}

ipaddressguide_body_data = {
        "ip": ""
}

service_option = -1

#validate IPv4 format (like 192.168.100.101)
def check_ip_format(ip):
    flag_ip_message_format = 1
    if ip.count(".") == 3:
        sub_ip = ip.split(".")
        for item in sub_ip:
            if str.isnumeric(item) and (0 <= int(item) <= 255):
                continue
            else:
                flag_ip_message_format = 0
                break
    else:
        flag_ip_message_format = 0
    return flag_ip_message_format

#request URL via POST and return HTML respnse
def post_request_service_url(url,header_data,body_data):
    new_request = requests.session()
    html_response = new_request.post(url, headers=header_data, data=body_data)
    return html_response.content

#request URL via GET and return HTML respnse
def get_request_service_url(url,header_data):
    new_request = requests.session()
    html_response = new_request.get(url, headers=header_data)
    return html_response.content

#parse NordVPN response
def parse_nordvpn(response):
    response_data = json.loads(response)
    return response_data

#parse ipaddressguide
def parsde_ipaddressguide(response):
    response_data = generic_response_structure
    raw_response_data = BeautifulSoup(response,"html.parser")
    data = ""
    data_elements = []
    for data in raw_response_data.find_all("td"):
        data_elements.append(data.get_text())
    if len(data_elements) > 0:
        response_data["country"] = data_elements[1]
        response_data["region"] = data_elements[2]
        response_data["city"] = data_elements[3]
        response_data["coordinates"]["latitude"] = data_elements[4]
        response_data["coordinates"]["longitude"] = data_elements[5]
        response_data["isp"] = data_elements[6]
    return response_data

#display parsed data
def display_parsed_data(response_data):
    string_data = "\n======================================" \
                + "\nCountry: " + response_data["country"] \
                + "\nCountry Code: " + response_data["country_code"] \
                + "\nLocation: " + response_data["location"] \
                + "\nRegion: " + response_data["region"] \
                + "\nCity: " + response_data["city"] \
                + "\nArea Code: " + response_data["area_code"] \
                + "\nISP: " + response_data["isp"] \
                + "\nLatitude: " + str(response_data["coordinates"]["latitude"]) \
                + "\nLongitude: " + str(response_data["coordinates"]["longitude"]) \
                + "\n======================================"
    return string_data

#CLI
os.system("clear")

#print(display_parsed_data(parsde_ipaddressguide(post_request_service_url("https://www.ipaddressguide.com//ip-geolocation",generic_header_data,ipaddressguide_body_data))))
#print(display_parsed_data(parse_nordvpn(get_request_service_url("https://nordvpn.com/wp-admin/admin-ajax.php?action=get_user_info_data&ip=193.106.191.223",generic_header_data))))

print(Fore.LIGHTGREEN_EX + "SIMPLE IP Cheker\nv1.0.0 by " + Fore.LIGHTYELLOW_EX + "@rizi85 \n ")

while service_option != 0:

    service_option = int(input(Fore.LIGHTBLUE_EX + "\nSelect a service to check with:\n\n 1. NordVPN \n 2. IpAddressGuide \n 0. Exit \n Select option: "))

    #NordVPN
    if service_option == 1:
        ip = input(Fore.LIGHTYELLOW_EX + "\n[>] Provide the IPv4 format: ")        
        try:
            if check_ip_format(ip) == 1:
                print(Fore.CYAN + "\n[=] Correct IPv4 format provided!")
                print(Fore.LIGHTGREEN_EX + "\n[+] NordVPN service response:")
                print(Fore.LIGHTGREEN_EX + display_parsed_data(parse_nordvpn(get_request_service_url(ip_services[1]+ip,generic_header_data))))
            else:
                print(Fore.LIGHTRED_EX + "\n[-] Wrong IPv4 format provided!")
        except:
            print(Fore.LIGHTRED_EX + "\n[-] Unable to load service!!!")
    #IpAddressGuide
    elif service_option == 2:
        ip = input(Fore.LIGHTYELLOW_EX + "\n[>] Provide the IPv4 format: ")        
        try:
            if check_ip_format(ip) == 1:
                print(Fore.CYAN + "\n[=] Correct IPv4 format provided!")
                print(Fore.LIGHTGREEN_EX + "\n[+] IpAddressGuide service response:")
                ipaddressguide_body_data["ip"] = ip
                print(Fore.LIGHTGREEN_EX + display_parsed_data(parsde_ipaddressguide(post_request_service_url(ip_services[2],generic_header_data,ipaddressguide_body_data))))
            else:
                print(Fore.LIGHTRED_EX + "\n[-] Wrong IPv4 format provided!")
        except:
            print(Fore.LIGHTRED_EX + "\n[-] Unable to load service!!!")