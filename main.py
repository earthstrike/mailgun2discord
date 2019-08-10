import hashlib
import hmac

import requests
import toml
from bottle import post, run, request, debug


def verify(api_key: bytes, token: bytes, timestamp: bytes, signature: bytes):
    "from mg docs"
    hmac_digest = hmac.new(
        key=api_key,
        msg="{}{}".format(timestamp, token).encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, hmac_digest)


@post("/mailgun/in")
def incoming_mg():
    print(request.json)
    if verify(
        MG_API_KEY,
        request.json["signature"]["token"],
        request.json["signature"]["timestamp"],
        request.json["signature"]["signature"],
    ):
        formatted_msg = f"{request.json['event-data']['event']} :thinking: \n{request.json['event-data']['recipient']} \n ```json\n{request.json['event-data']['delivery-status']}```"
        shove2discord(formatted_msg)


def shove2discord(msg):
    ret = requests.post(DISCORD_URL, data={"content": msg})
    ret.raise_for_status()


if __name__ == "__main__":
    conf = toml.load("config.toml")
    MG_API_KEY = conf["mg_signing_key"].encode()
    DISCORD_URL = conf["discord_webhook_url"]
    # shove2discord("testing")
    debug(True)
    run(reloader=True)
