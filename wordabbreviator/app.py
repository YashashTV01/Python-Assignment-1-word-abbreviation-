from flask import Flask, render_template, request
from FirstAss import nameAbbreviator
import re
import numpy as np

app = Flask(__name__)

# Load values once during startup
def load_position_values():
    letters = []
    values = []
    with open('resources/values.txt', encoding='utf-8') as file:
        for line in file:
            parts = line.rstrip().split()
            if len(parts) == 2:
                letters.append(parts[0])
                values.append(int(parts[1]))
    postn_values = dict(zip(letters, values))
    return dict(sorted(postn_values.items(), key=lambda x: x[1]))

sorted_postn_values = load_position_values()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')
    if uploaded_file and uploaded_file.filename.endswith('.txt'):
        content = uploaded_file.read().decode('utf-8')
        result = generate_abbreviations(content)
        return render_template('index.html', result=result)
    return render_template('index.html', result="❌ Invalid file uploaded.")

@app.route('/abbreviate', methods=['POST'])
def abbreviate():
    single_word = request.form.get('singleWord')
    if single_word:
        result = generate_abbreviations(single_word)
        return render_template('index.html', result=result)
    return render_template('index.html', result="❌ Please enter a word.")

def clean_text(text):
    text = text.upper().replace("'", "")
    text = re.sub('[^A-Z \n]', ' ', text)
    text = re.sub('\s+', ' ', text)
    return text.strip()

def generate_abbreviations(text):
    lines = text.strip().split('\n')
    results = []
    for line in lines:
        clean_line = clean_text(line)
        if clean_line:
            abbr, score = nameAbbreviator(clean_line, sorted_postn_values)
            score_display = score if not np.isnan(score) else 'N/A'
            # Put abbreviation on the same line as the name with colon and space
            results.append(f"{clean_line}: {abbr} (Score: {score_display})")


    return "\n".join(results)

if __name__ == '__main__':
    app.run(debug=True)
