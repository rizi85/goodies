#passwd reader

import sys

class Rpasswd:
    def __init__(self, filePath):
        self.filePath = filePath

    #Read and parsse file content and construct dictionary
    def fileParss(self):

        #Create an empty  dictionary to put data from passwd file. Format will be:
        passwdContent = {
            "user" : [],
            "encriptPass" : [],
            "homeDir" : [],
            "shell" : []
        }
        
        #Try open file for read or trow exeption
        try:
            fileName = open(self.filePath, "r+")
        except OSError:
            print("[!] Could not open file: " + self.filePath)
            print("[!] Please check file path or file name!" )
            sys.exit()

        #Iterate thru file and add data to dictionary
        with open(self.filePath) as fileName:
            for line in fileName:
                lineSplit = line.split(":")

                #Add user to dictionary
                passwdContent["user"].append(lineSplit[0])

                #Add encriptPass to dictionary
                passwdContent["encriptPass"].append(lineSplit[1])

                #Add homeDir to dictionary
                passwdContent["homeDir"].append(lineSplit[5])

                #Add shell to dictionary
                passwdContent["shell"].append(lineSplit[6])

        #Close file
        fileName.close()

        #return constructed passwdContent dictionary
        return passwdContent

    #Check unencrypted passwords - no "x" on second column. Retun True if any found!
    def checkUnencryptedPasswords(self, myDictionary):

        #Check dictionary not empty
        if len (myDictionary) != 0:

            #Set flag for evaluation
            flag = False

            #Determin position of checked value
            index = 0

            #Check each password encryption sign and return user and home dir for unencrypted ones
            for value in myDictionary["encriptPass"]:

                if value != "x":
                    #Print user with unencrypted password
                    print("[+] " + str(myDictionary["user"][index]) + " use unencrypted password!")
                    #Print home dir for same user
                    print(" |-> [+] Home path: " + str(myDictionary["homeDir"][index]) + "\n")
                    flag = True

                #Increment index
                index = index + 1

        #Evaluate flag
        if not flag:    
            print("[-] No user found with unencrypted password!\n")

    #Check user had shell access - no /false or /nologin on last column!
    def checkUserShell(self, myDictionary):
        
        #Check dictionary not empty
        if len (myDictionary) != 0:

            #Set flag for evaluation
            flag = False

            #Determin position of checked value
            index = 0

            #Check each shell path and return user and home dir for the ones with access
            for value in myDictionary["shell"]:
                if (not "nologin" in value) and (not "false" in value):
                    #Print user with shell access
                    print("[+] " + str(myDictionary["user"][index]) + " has shell access!")
                    #Print home dir for same user
                    print(" |-> [+] Home path: " + str(myDictionary["homeDir"][index]))
                    #Print shell dir for same user
                    print(" |-> [+] Shell path: " + str(myDictionary["shell"][index]) + "\n")
                    flag = True

                #Increment index
                index = index + 1

        #Evaluate flag
        if not flag:    
            print("[-] No user found with shell access! \n")

    #Check user had shell access - no /false or /nologin on last column! Check unencrypted passwords - no "x" on second column. Retun True if any found!
    def checkUserUnencryptedPassShellAccess(self, myDictionary):
        #Check dictionary not empty
        if len (myDictionary) != 0:

            #Set flag for evaluation
            flag = False

            #Determin position of checked value
            index = 0

            #Check each shell path and password and return user and home dir for the ones with access
            for value in myDictionary["shell"]:
                if (not "nologin" in value) and (not "false" in value) and (str(myDictionary["encriptPass"][index]) != "x"):
                    #Print user with shell access
                    print("[+] " + str(myDictionary["user"][index]) + " has full access!")
                    #Print home dir for same user
                    print(" |-> [+] Home path: " + str(myDictionary["homeDir"][index]))
                    #Print shell dir for same user
                    print(" |-> [+] Shell path: " + str(myDictionary["shell"][index]) + "\n")
                    flag = True

                #Increment index
                index = index + 1

        #Evaluate flag
        if not flag:    
            print("[-] No user found with full access! \n")

#=============== MAIN ===============

#PATH TO FILE
FILE = "passwd"

#Initialize script
newPasswd = Rpasswd(str(FILE))
dataDictionary = newPasswd.fileParss()
print("=======================\nSTART RPasswd\n=======================\nv 1.0.0\n-----------------------\n")

#Check users with full access
print("[!] Check for users with full access! \n")
newPasswd.checkUserUnencryptedPassShellAccess(dataDictionary)

#Check users with unencrypted passwords
print("[!] Check for users with unencrypted password! \n")
newPasswd.checkUnencryptedPasswords(dataDictionary)

#Check users shell access
print("[!] Check for users with shell access! \n")
newPasswd.checkUserShell(dataDictionary)