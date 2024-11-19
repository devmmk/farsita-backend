from flask import Flask
from requests import *

app = Flask(__name__)

def text_to_text(src_lang, dst_lang, text):
    url = 'https://api.reverso.net/translate/v1/translation'
    headers = {
        'content-type':'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0'
    }
    data = {"format":"text","from":src_lang,"to":dst_lang,"input": text,"options":{"origin":"translation.web"}}
    try:
        request = post(url, headers=headers, json=data)
        return(request.text)
    except BaseException as e:
        print(e)

print(text_to_text("eng", "per", "hello world"))

"""
@app.route("/")
def handler():
    return text_to_text("eng", "per", "hello stupid asses")

if __name__ == "__main__":
    app.run()
"""