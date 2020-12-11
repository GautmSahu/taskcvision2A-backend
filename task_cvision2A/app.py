import os

from flask import Flask, request, jsonify, make_response,render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
UPLOAD_FOLDER = os.getcwd()+"/uploadedImages/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Images(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(200))


@app.route('/')
def homepage():
	return "Homepage."

@app.route('/upload',methods=["POST"])
def upload():
	fle = request.files['img']
	filename = secure_filename(fle.filename)
	img = Images(
		filename=filename,
	)
	db.session.add(img)
	db.session.commit()
	fle.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	result={'valid':filename}
	return result


if __name__ == "__main__":
	app.run(debug = True)
