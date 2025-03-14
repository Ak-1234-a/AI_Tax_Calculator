from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
from invoice_processor import process_invoice  # Extracts invoice details
from classification import classify_transaction  # Classifies transactions

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample AI-based deduction suggestions (Can be improved with NLP & ML)
def get_tax_deductions(description, amount):
    suggestions = []
    if "travel" in description.lower():
        suggestions.append("🚗 Consider deducting travel expenses.")
    if "meal" in description.lower() or "restaurant" in description.lower():
        suggestions.append("🍽️ Business meals may be partially deductible.")
    if "software" in description.lower() or "subscription" in description.lower():
        suggestions.append("💻 Software and SaaS subscriptions may be tax-deductible.")
    if "training" in description.lower() or "education" in description.lower():
        suggestions.append("📚 Training & education expenses may be deductible.")
    if amount >= 800:
        suggestions.append("🔍 Large transactions might qualify for capital expense deductions.")

    return suggestions

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
        # Process invoice to extract relevant data
        extracted_data = process_invoice(filepath)

        # Extract transaction description & amount
        description = extracted_data.get("description", "Unknown transaction")
        amount = extracted_data.get("amount", 0)

        # Classify transaction as Taxable or Non-Taxable
        tax_classification = classify_transaction(description, amount)
        extracted_data["tax_classification"] = tax_classification  # Add classification result

        # Get tax deduction suggestions if taxable
        extracted_data["deduction_suggestions"] = get_tax_deductions(description, amount) if tax_classification == "Taxable" else []

        return jsonify(extracted_data)
    
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
