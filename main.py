import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

jsonData = json.load(open("./config.json", "r"))
params = jsonData['params']
local_server = params['local_server']

app = Flask(__name__, template_folder='templates')

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['user-gmail'],
    MAIL_PASSWORD=params['pass-gmail']
)

mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_db_uri'] if local_server else params['prod_db_uri']

db = SQLAlchemy(app)
print(db)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12),  unique=True, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),  unique=True, nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    subtitle = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(),  unique=True, nullable=False)
    content = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime())


@app.route("/")
def home_page():
    posts = Posts.query.filter_by().all()
    return render_template('index.html', posts=posts)


@app.route("/about")
def about_route():
    name = "Shashwat"
    return render_template("about.html", name=name)


@app.route("/home")
def login():
    name = "Shashwat"
    return render_template("login.html", name=name)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", post=post)


@app.route("/contact", methods=["GET", "POST"])
def contact_route():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        data_to_sub = Contacts(name=name, phone=phone,
                               email=email, message=message)
        print(data_to_sub, type(data_to_sub))
        db.session.add(data_to_sub)
        db.session.commit()
        mail.send_message('New message from' + name,
                          sender=email, recipients=[params['user-gmail']],
                          body=message + "\n" + phone
                          )

    return render_template("contact.html")


app.run(debug=True)
