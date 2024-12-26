import os
import subprocess
import time
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>BibTeX to XML Converter</title>
    <h1>Upload a BibTeX file to convert to XML</h1>
    <form method="post" action="/api/bib2xml" enctype="multipart/form-data">
      <input type="file" name="file"><br>
      <input type="submit" value="Convert">
    </form>
    '''

@app.route('/api/bib2xml', methods=['POST'])
def bib2xml():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.bib'):
        script_dir = os.path.dirname(__file__)
        tmp_dir = os.path.join(script_dir, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        
        input_path = os.path.join(tmp_dir, file.filename)
        output_path = input_path.replace('.bib', '.xml')
        file.save(input_path)

        try:
            # Note that there is no -o flag. The output has to be saved separately.
            with open(output_path, 'w') as output_file:
                subprocess.run(['bib2xml', input_path], stdout=output_file, check=True)
            
            start_time = time.time()
            timeout_s = 3
            while time.time() - start_time < timeout_s:
                if os.path.exists(output_path):
                    return send_file(output_path, as_attachment=True)
                time.sleep(0.1)
            
            return "Error converting file", 500
        except subprocess.CalledProcessError:
            return "Error converting file", 500
        finally:
            os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)