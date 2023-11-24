
# Importing necessary libraries
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

# Creating a Flask app instance
app = Flask(__name__)

# Route for serving the HTML form
@app.route('/')
def index():
    # Render an HTML form for file upload
    return render_template('index.html')

# Route for handling the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        # Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)
        file.save(os.path.join('data', filename))
        return 'File successfully uploaded'

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
