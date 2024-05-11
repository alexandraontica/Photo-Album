from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import secrets
import os
import re
from PIL import Image

app = Flask(__name__, static_folder="public")

secret_key = secrets.token_hex(16)
app.secret_key = secret_key # required by session

users = {
    'felix_motanul': 'miau123!',
}

UPLOAD_FOLDER = '/usr/src/app/public/upload'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return filename.lower().endswith(('png', 'jpg', 'jpeg'))

def remove_special_characters(text):
    pattern = r'[^a-zA-Z0-9.\s]'  # any character that is not alphanumeric or '.'
    sanitized_text = re.sub(pattern, '', text)
    return sanitized_text

@app.route('/')
def home():
    logged_in = session.get('logged_in', False)
    
    categories = []
    for entry in os.scandir(app.config['UPLOAD_FOLDER']):
        if entry.is_dir():
            categories.append(entry.name)

    thumbnail_paths = {}
    for category in categories:
        category_dir = os.path.join(app.config['UPLOAD_FOLDER'], category)
        
        image_files = []
        for entry in os.scandir(category_dir):
            if entry.is_file():
                image_files.append(entry.name)

        thumbnail_files = []
        for file in image_files:
            if file.endswith('.thumb' + os.path.splitext(file)[1]):
                thumbnail_files.append(file)

        thumbnail_paths[category] = []
        for file in thumbnail_files:
            thumbnail_paths[category].append(os.path.join(category, file))
    return render_template('home.html', logged_in=logged_in, thumbnail_paths=thumbnail_paths)

@app.route('/upload/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/aboutme')
def aboutme():
    logged_in = session.get('logged_in', False)
    return render_template('aboutme.html', logged_in=logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/upload')
def upload_page():
    logged_in = session.get('logged_in', False)
    return render_template('upload.html', logged_in=logged_in)

@app.route('/upload-file', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    name = request.form['name']
    category = request.form['category']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        category_dir = os.path.join(app.config['UPLOAD_FOLDER'], category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        filename = file.filename
        filename = filename.replace(" ", "")
        filename = remove_special_characters(filename)
        file.save(os.path.join(category_dir, filename))
        
        img = Image.open(os.path.join(category_dir, filename))
        img.thumbnail((200, 200))
        thumbnail_filename = os.path.splitext(filename)[0] + '.thumb' + os.path.splitext(filename)[1]
        img.save(os.path.join(category_dir, thumbnail_filename))
        
        return redirect(url_for('home'))
    else:
        return redirect(request.url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
