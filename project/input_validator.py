import re
import socket

# Used in other files to validate inputs

class Validator():
    def __init__(self) -> None:
        pass

    #Checks if input is a valid number
    def check_num(input_string):
        try:
            regex = r'^[0-9]+$'
            if bool(re.match(regex, int(input_string))):
                return True
        except:
            return False
        
    #Checks if input is a valid text string. No Special characters are accepted except '.'
    def check_string(input_string):
        try:
            regex = r'^[a-zA-Z0-9.]+$'
            if bool(re.match(regex, input_string)):
                return True
        except:
            return False
        
    #Checks if input is a valid text string. No Special characters are accepted except '.', '!'
    def check_passwd(input_string):
        try:
            regex = r'^[a-zA-Z0-9!.]+$'
            if bool(re.match(regex, input_string)):
                return True
        except:
            return False
    #Checks if input is a valid text string. No Special characters are accepted except '.', ','
    def check_street(input_string):
        try:
            regex = r'^[a-zA-Z0-9,.]+$'
            if bool(re.match(regex, input_string)):
                return True
        except:
            return False
    
    #Checks if input is a valid ip address
    def check_ip(input_string):
        try:
            socket.inet_aton(input_string)
            return True
        except:
            return False