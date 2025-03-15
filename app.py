from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os

app = Flask(__name__)

# Fetch the API Key from environment variable (ensure it is set)
my_api_key_gemini = os.getenv('AIzaSyCyzNTp8n12KOJ9wGw8cnV_ix9BPslk5yk')  # Make sure you've set this in your environment variables
genai.configure(api_key="AIzaSyCyzNTp8n12KOJ9wGw8cnV_ix9BPslk5yk")

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

# Define your 404 error handler to redirect to the index page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            print(f"User prompt: {prompt}")

            # Generate content using Gemini's model
            response = model.generate_content(prompt)  # Ensure this is the correct method for generating content
            print(type(response))
            print(response.result)
            print(response.result['candidates'][0]['content']['parts'][0]['text'])
            # Extracting the text from the response
            if response and 'result' in response and 'candidates' in response.result:
                candidates = response.result['candidates']
                if candidates:
                    content = candidates[0].get('content', {})
                    parts = content.get('parts', [])
                    if parts:
                        text = parts[0].get('text', '')
                        return text  # Return the extracted text
                return "Sorry, but Gemini didn't want to answer that!"
            else:
                return "Sorry, but Gemini didn't want to answer that!"
        except Exception as e:
            return f"Sorry, but Gemini didn't want to answer that! Error: {str(e)}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
