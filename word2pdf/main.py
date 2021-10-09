# -*- coding: utf-8 -*-
"""
@Date    : 2021/9/30
@Author  : libaibuaidufu
@Email   : libaibuaidufu@gmail.com
"""
import os
import uuid
from os.path import exists

from flask import Flask, request, send_from_directory, jsonify, render_template, url_for, make_response

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload_files')
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.getcwd(), 'download_files')

if not exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

if not exists(app.config['DOWNLOAD_FOLDER']):
    os.mkdir(app.config['DOWNLOAD_FOLDER'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_file', methods=["POST"])
def upload_file():
    file = request.files.get('file')
    file_name, file_type = file.filename.rsplit('.', 1)
    uuid_file_name = uuid.uuid4()
    uuid_file_type_name = f'{uuid_file_name}.{file_type}'
    uuid_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid_file_type_name)
    file.save(uuid_file_path)
    if file_type == 'pdf':
        upload_type = 'docx'
        old_file_pdf_name = f"{file_name}.docx"
        os.system(
            f'soffice --headless --invisible --infilter="writer_pdf_import" --convert-to docx {uuid_file_path} --outdir {app.config["DOWNLOAD_FOLDER"]}')
        uuid_file_pdf_name = f'{uuid_file_name}.docx'
    else:
        upload_type = 'pdf'
        old_file_pdf_name = f"{file_name}.pdf"
        os.system(
            f'soffice --headless --invisible --convert-to pdf {uuid_file_path} --outdir {app.config["DOWNLOAD_FOLDER"]}')
        uuid_file_pdf_name = f'{uuid_file_name}.pdf'

    result_dict = {
        'data': {'url': url_for('.download_file', filename=uuid_file_pdf_name, file_name=old_file_pdf_name),
                 'file_name': old_file_pdf_name, 'type': upload_type}
    }
    return jsonify(result_dict)


@app.route('/download_file/<filename>')
def download_file(filename):
    file_name_type = request.args.get("file_name")
    if file_name_type:
        print(file_name_type)
        response = make_response(send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            file_name_type.encode().decode('latin-1'))
        return response
    else:
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
