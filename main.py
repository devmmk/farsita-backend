from flask import Flask
import io, json

app = Flask(__name__)

class Translate:
    def __init__(self):
        self.url = 'https://api.reverso.net/translate/v1/translation'
        self.headers = {
            'content-type':'application/json',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0'
        }
        
    def text_to_text(self, src_lang, dst_lang, text):
        data = {"format":"text","from":src_lang,"to":dst_lang,"input": text,"options":{"origin":"translation.web"}}
        try:
            request = post(url=self.url, headers=self.headers, json=data)
            result = request.json()
            return result['translation'][0]
        except BaseException as e:
            print(e)
    
    def sound_to_text(self, src_lang, dst_lang, sound_path):
        try:
            result = transcribe_audio(sound_path, src_lang)
        except BaseException as e:
            print(e)
        
        return result

@app.route("/")
def handler():
    return "hello world"

if __name__ == "__main__":
    translate = Translate()
    app.run()
