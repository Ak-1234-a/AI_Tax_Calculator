from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
from invoice_processor import process_invoice  # Correct function import

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/Dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/getstarted', methods=['POST'])
def get_started():
    return redirect(url_for('dashboard'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        extracted_data = process_invoice(filepath)  # Use the correct function
        return jsonify(extracted_data)
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
