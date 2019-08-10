import hashlib
import hmac


import requests
import toml
from bottle import post, run, request

def verify(api_key, token, timestamp, signature):
    "from mg docs"
    hmac_digest = hmac.new(key=api_key,msg='{}{}'.format(timestamp, token),digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(unicode(signature), unicode(hmac_digest))

@post("/mailgun/in")
def incoming_mg():
    print(request.json)

def shove2discord(msg):
    ret = requests.post(DISCORD_URL, data={'content': "pee pee poo poo"})
    ret.raise_for_status()

if __name__ == "__main__":
    conf = toml.load("config.toml")
    MG_API_KEY  = conf["mg_signing_key"]
    DISCORD_URL = conf["discord_webhook_url"]
    shove2discord("testing")
    run()