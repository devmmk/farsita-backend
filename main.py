from flask import Flask
from requests import *

app = Flask(__name__)

def text_to_text(src_lang, dst_lang, text):
    url = 'https://api.reverso.net/translate/v1/translation'
    headers = {
        'content-type':'application/json',
        'user-agent': 'Cy'
    }
    data = {"format":"text","from":src_lang,"to":dst_lang,"input": text,"options":{"origin":"translation.web"}}
    try:
        request = get(url, headers=headers, data=data)
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