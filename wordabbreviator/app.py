from flask import Flask, render_template, request, jsonify
from FirstAss import abbreviator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    path = request.form['path']
    abbreviator(path)

    input_filename = path.split('/')[-1].split('.')[0].lower()
    surname = 'Yashash'
    output_name = f'output/{surname}_{input_filename}_abbrevs.txt'

    try:
        with open(output_name, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = "Output file not found."


    return jsonify(result=content)

if __name__ == '__main__':
    app.run(debug=True)
