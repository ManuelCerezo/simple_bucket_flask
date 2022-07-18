from flask import Flask, request,render_template,Response
from werkzeug.utils import secure_filename
from config import SQLALCHEMY_DATABASE_URI_SQLITE,SQLALCHEMY_TRACK_MODIFICATIONS 
from db import init_db,db
from models import Img

app = Flask(__name__,template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_SQLITE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

init_db(app)

pictures = []

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload',methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return "not pic allowed",400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Img(img=pic.read(), mimetype = mimetype, name = filename, )
    db.session.add(img)
    db.session.commit()
    return "OK",200

@app.route('/get-image/<int:id>',methods=['GET'])
def get_image(id):
    img = Img.query.filter_by(id = id).first()
    if not img:
        return "img not allowed"
    return Response(img.img, mimetype = img.mimetype)

@app.route('/dropzone',methods=['GET'])
def dropzone():
    return render_template('drag_drop.html')

@app.route('/dropzone/images/<int:type>',methods=['POST'])
def dropzone_upload(type):

    if type == 1:
        pic = request.files['file']
        pictures.append(Img(img=pic.read(), mimetype = pic.mimetype, name = secure_filename(pic.filename), ))
        return "",200

    if type == 2:
        add_to_sql()
        return {"estado":"subido"},200
    
    


def add_to_sql():
    for pic in pictures:
        db.session.add(pic)
        
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)