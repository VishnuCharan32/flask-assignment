from flask import Flask, render_template, request, jsonify
import os
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  
app.secret_key = 'abc@123'  

db = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            raise Exception('No file part')

        file = request.files['file']

        if file.filename == '':
            raise Exception('No selected file')

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            upload_timestamp = datetime.datetime.now().strftime("%d %B %Y")
            file_format = filename.split('.')[-1]
            file_size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)) / (1024 * 1024)  

            db.append({
                'filename': filename,
                'filesize': f'{file_size:.2f} MB',
                'Uploaded_on': upload_timestamp,
                'Format': file_format,
                'Path': os.path.join(app.config['UPLOAD_FOLDER'], filename)
            })

            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'filesize': f'{file_size:.2f} MB',
                'Uploaded_on': upload_timestamp,
                'Format': file_format,
                'Path': os.path.join(app.config['UPLOAD_FOLDER'], filename)
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_metadata', methods=['POST'])
def get_metadata():
    try:
        data = request.get_json()
        filename = data.get('filename')

        for file_metadata in db:
            if file_metadata['filename'] == filename:
                return jsonify(file_metadata), 200

        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
