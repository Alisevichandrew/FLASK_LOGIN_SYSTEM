import os
from os import name
from flask import request
from flask import Flask 
from flask import render_template, redirect #берет 'index.py' и заменяет вставки на 'HTML'
#from flask import Flask, request, render_template, redirect
UPLOAD_FOLDER = 'C:\\Users\\HP\\FLASK_LOGIN_SYSTEM' #папка для загрузки
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
@app.route('/index', methods=['GET'])
def index():
    print(request.method)
    return 'Hello world'

@app.route('/form', methods=['GET', 'POST'])
def form_show():
    if request.method == 'GET': 
        return """
        <form action='http://127.0.0.1:5000/form' method='POST'>
        <p>Name: <input type='text' name=Name /></p>    
        <p>Math: <input type='number' name=Math /></p>
        <p>CS: <input type='password' name=CS /></p>
        <p><input type='submit'></p>
        </form>
        """     
    result = request.form
    return render_template('circle.html', result=result) 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        filename = file.filename
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # загрузка файла
        return 'Ok'
 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


 
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) # 'debug=True' - консоль будет автоматически обновляться
