import os
from pathlib import Path

from PIL import Image

from app import app
from flask import request, redirect, render_template, flash, session
from . image_metadata import ImageMetaData, get_metadata_from_file

app.config['UPLOAD_FOLDER'] = Path(__file__).parent / "static"
app.config['SECRET_KEY'] = 'sdsdadds'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',  methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == "POST":
        file = request.files['filename']
        filename = "image.jpg"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "images", filename)

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('File must be an image')
            return redirect(request.url)
        try:
            file.save(file_path)
            flash("succesfully uploaded image file")

        except Exception as e:
            print("file save error", e)
        imd = get_metadata_from_file(Path(file_path))
        data['device'] = imd.device
        data['width'] = imd.width_px
        data['height'] = imd.height_px
        data['date taken'] = imd.datetime

        return render_template("main.html", data=data, image=filename)
    # Clear any flashed messages from the session before rendering the template
    session.pop('_flashes', None)
    return render_template("main.html")
