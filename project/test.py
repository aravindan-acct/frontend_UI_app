from flask import Flask

app = Flask(__name__)

print(__name__)

def test():
    print(__name__)

test()

