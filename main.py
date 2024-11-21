from flask import Flask, request, jsonify, send_file, render_template
from openai import OpenAI
import io, json, os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import speech_recognition as sr
from requests import post, get
import pyttsx3

class Translate:
    def __init__(self):
        self.url = 'https://api.reverso.net/translate/v1/translation'
        self.headers = {
            'content-type':'application/json',
            'user-agent': 'Cy'
        }
    
    # lang input: eng, per
    def text_to_text(self, src_lang, dst_lang, text):
        data = {
            "format": "text",
            "from": src_lang,
            "to": dst_lang,
            "input": text,
            "options": {"origin": "translation.web"}
        }
        try:
            request = post(url=self.url, headers=self.headers, data=json.dumps(data))
            result = request.json()
            return result['translation'][0]
        except BaseException as e:
            print(e)
    
    
    # lang input: fa-IR, en-US
    def transcribe_audio(self, audio_path, lang="fa-IR"):
        with sr.AudioFile(audio_path) as source:
            r = sr.Recognizer()
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data, language=lang)
            return text
        
    
    def sound_to_text(self, src_lang, dst_lang, sound_path):
        try:
            result = self.transcribe_audio(sound_path, src_lang)
        except BaseException as e:
            print(e)
        else:
            translated = self.text_to_text(src_lang, dst_lang, result)
            return translated
            
    
    def image_to_text(self, src_lang, dst_lang, image_path):
        try:
            image = Image.open(image_path)
            image = image.convert('L')
            image = image.filter(ImageFilter.SHARPEN)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            text = pytesseract.image_to_string(image,  lang=src_lang)
        except BaseException as e:
            print(e)
        else:
            #TODO change the src lang to something else
            translated = self.text_to_text(src_lang, dst_lang, text)
            return translated
    
    def text_to_speech(self, text, dst_lang):
        engine = pyttsx3.init(driverName='espeak')
        engine.setProperty('voice', 'fa')  # Set Persian language
        engine.setProperty('rate', 150)  # Adjust speed
        engine.say(text)
        engine.save_to_file(text, "output.mp3")
        engine.runAndWait()
        return "output.mp3"

"""
class AIChatBot:
    def __init__(self):         
        self.base_url = "https://api.aimlapi.com/v1"
        self.api_key = "c9182ee11f9e4d97910c994c17e6781c"
        self.api = OpenAI(api_key=self.api_key, base_url=self.base_url)


    def talk_to_ai(self, text):
        messages=[
                {"role": "system", "content": "You are a language learning assistant and partner to improving language skills."},
                {"role": "user", "content": text},
        ]

        completion = self.api.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=256,
        )

        response = completion.choices[0].message.content
        return response
"""

class AIChatBot:
    def __init__(self):
        self.url = "https://api3.haji-api.ir/majid/gpt/4?q={}&license=HPegOmZxczNMUNLG38IZWSH4WHFuaWCBVYdt8Iu1AfIGjBVMo71fZA0idUd"
        self.role = "You are a language learning assistant and partner to improving language skills. here is the user text:\n\n"
    
    def talk_to_ai(self, text):
        response = get(self.url.format(self.role + text))
        return response.json()['result']
        

app = Flask(__name__)
translate = Translate()
ai = AIChatBot()

@app.route("/")
def handler():
    return "Hello World!"

@app.route("/text", methods=['POST'])
def text_handler():
    data = request.get_json()
    src_lang = data.get('src_lang')
    dst_lang = data.get('dst_lang')
    text = data.get('text')
    result = translate.text_to_text(src_lang, dst_lang, text)
    return jsonify({"translation": result})

@app.route("/audio", methods=['POST'])
def audio_handler():
    data = request.files['audio']
    src_lang = request.form.get('src_lang')
    dst_lang = request.form.get('dst_lang')
    
    temp_path = "temp_audio.wav"
    data.save(temp_path)
    
    translate = Translate()
    result = translate.sound_to_text(src_lang, dst_lang, temp_path)
    
    os.remove(temp_path)
    return jsonify({"translation": result})

@app.route("/image", methods=['POST'])
def image_handler():
    data = request.files['image']
    src_lang = request.form.get('src_lang')
    dst_lang = request.form.get('dst_lang')
    
    temp_path = "temp_image.png"
    data.save(temp_path)
    
    translate = Translate()
    result = translate.image_to_text(src_lang, dst_lang, temp_path)
    
    os.remove(temp_path)
    return jsonify({"translation": result})

@app.route("/ai-chat", methods=['GET'])
def ai_chat_handler():
    # return the index.html file
    return render_template('./index.html')

@app.route("/ai", methods=['POST'])
def ai_chatbot():
    print(request)
    print(request.form)
    data = request.form.get('message')
    return ai.talk_to_ai(data)

@app.route("/tts", methods=['POST'])
def speech_handler():
    data = request.form.get('message')
    dst_lang = request.form.get('dst_lang')
    result = translate.text_to_speech(data, dst_lang)
    return send_file(result, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
