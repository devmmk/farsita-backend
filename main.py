from flask import Flask
import io, json
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

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
    
    def image_to_text(self, src_lang, dst_lang, image_path):
        try:
            image = Image.open(image_path)
            image = image.convert('L')
            image = image.filter(ImageFilter.SHARPEN)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            text = pytesseract.image_to_string(image,  lang=src_lang)
            return(text)
        except BaseException as e:
            print(e)

@app.route("/")
def handler():
    return "hello world"

if __name__ == "__main__":
    translate = Translate()
    app.run()
