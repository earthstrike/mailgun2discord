import requests
from bottle import post, run, request

@post("/mailgun/in")
def incoming_mg():
    print(request.json)

if __name__ == "__main__":
    run()