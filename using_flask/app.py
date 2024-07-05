from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

def get_gemini_response(input_text, image_path, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        image_parts = [
            {
                "mime_type": 'image/jpeg',  # Update this based on the image type
                "data": image_data
            }
        ]
        response = model.generate_content([input_text, image_parts[0], prompt])
        return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    image_path = None
    input_text = ''

    if request.method == 'POST':
        input_text = request.form['input']
        uploaded_file = request.files['file']
        if uploaded_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            input_prompt = """
                You are an expert in understanding invoices.
                You will receive input images as invoices &
                you will have to answer questions based on input image
            """
            response = get_gemini_response(input_text, file_path, input_prompt)
            image_path = file_path

    return render_template('index.html', response=response,input=input_text, image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
