import re
import socket

class Validator():
    def __init__(self) -> None:
        pass

    def check_num(input_string):
        try:
            regex = r'^[0-9]+$'
            if bool(re.match(regex, int(input_string))):
                return True
        except:
            return False
    
    def check_string(input_string):
        try:
            regex = r'^[a-zA-Z0-9.]+$'
            if bool(re.match(regex, input_string)):
                return True
        except:
            return False

    def check_passwd(input_string):
        try:
            regex = r'^[a-zA-Z0-9!.]+$'
            if bool(re.match(regex, input_string)):
                return True
        except:
            return False

    def check_street(input_string):
        try:
            regex = r'^[a-zA-Z0-9,.]+$'
            if bool(re.match(regex, input_string)):
                return True
        except:
            return False

    def check_ip(input_string):
        try:
            socket.inet_aton(input_string)
            return True
        except:
            return False