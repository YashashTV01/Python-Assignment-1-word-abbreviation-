from flask import Flask, render_template, request, send_file
import os
from FirstAss import abbreviator
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    abbreviator(filepath)  # Calls your main function

    # Prepare the output filename
    input_filename = filename.split('.')[0].lower()
    output_filename = f"Yashash_{input_filename}_abbrevs.txt"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return 'Output file not generated.', 500

if __name__ == '__main__':
    app.run(debug=True)
