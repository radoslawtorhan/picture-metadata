import os
from pathlib import Path

from app import app
from flask import request, redirect, render_template, flash
from . image_metadata import ImageMetaData, get_metadata_from_file

app.config['UPLOAD_FOLDER'] = r"C:\Users\Radek\Desktop\Python simple projects\web-flask-picture-metadata\app\static"

@app.route('/',  methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == "POST":
        file = request.files['filename']
        filename = "image.jpg"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "images", filename)
        try:
            file.save(file_path)
        except Exception as e:
            print(e)

        imd = get_metadata_from_file(Path(file_path))
        data['device'] = imd.device
        data['width'] = imd.width_px
        data['height'] = imd.height_px
        data['date taken'] = imd.datetime

        return render_template("main.html", data=data, image=filename)
    return render_template("main.html")