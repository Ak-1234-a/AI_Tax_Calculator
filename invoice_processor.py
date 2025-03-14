import pdfplumber

def process_invoice(filepath):
    extracted_data = {
        "invoice_number": "Unknown",
        "date": "Unknown",
        "client": "Unknown",
        "amount": 0.0,
        "tax": 0.0
    }

    try:
        with pdfplumber.open(filepath) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        for line in text.split("\n"):
            if "Invoice Number" in line:
                extracted_data["invoice_number"] = line.split(":")[-1].strip()
            if "Date" in line:
                extracted_data["date"] = line.split(":")[-1].strip()
            if "Client" in line:
                extracted_data["client"] = line.split(":")[-1].strip()
            if "Total Amount" in line:
                extracted_data["amount"] = float(line.split(":")[-1].strip().replace("$", ""))
            if "Tax" in line:
                extracted_data["tax"] = float(line.split(":")[-1].strip().replace("$", ""))
    except Exception as e:
        print(f"Error processing invoice: {e}")

    return extracted_data
