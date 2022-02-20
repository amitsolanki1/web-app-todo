import datetime
from flask import Flask,render_template,flash,url_for,redirect,request,session

# pip install Flask-SQLALchemy
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
# import pymysql
# engine=create_engine("mysql+pymysql://root:123456@localhost/register")
                    #(mysql+pymysql://username:password@localhost/database)
# db=scoped_session(sessionmaker(bind=engine))
app=Flask(__name__)
app.secret_key='3278ysdhkjbdshjg_$dshk37'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    email=db.Column(db.String(100))
    pwd=db.Column(db.String(100))
    mobile=db.Column(db.Integer)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    description=db.Column(db.String(300))
    time_=db.Column(db.String(50))
    complete=db.Column(db.Boolean)
@app.route("/")
def home():
    # insert data into table
    # new_todo=Todo(title="notes 2",description="this is my second note",complete=False)
    # db.session.add(new_todo)
    # db.session.commit()
    notes=Todo().query.all()
    # if session.log:
    #     print(session.log)
    #     user_email=session.log
    #     user_pwd=session.pwd
    #     res=users.query.filter_by(email=user_email,pwd=user_pwd).first()
    #     if res:
    # # print(notes)
    #         return render_template("index.html",all_data=notes,data=res)
    # else:
    return render_template("index.html",all_data=notes)
        

@app.route("/add_new",methods=['POST'])
def add():
    if request.method=="POST":
        title=request.form.get("title")
        desc=request.form.get("desc")
        t=datetime.datetime.now()
        new_notes=Todo(title=title,description=desc,time_=t,complete=False)
        db.session.add(new_notes)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form.get('desc')#["desc"]
        t=datetime.datetime.now()
        res=Todo.query.filter_by(id=sno).first()
        if res:
            res.id=sno
            res.title=title
            res.description=desc
            res.time_=t
            db.session.commit()
            flash("Updated sucessfully!","grey lighten-2")
            return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))
    else:
        # res=Todo.query.filter_by(id=sno).first()
        # res.complete=not res.complete
        # db.session.commit()
        res=sno
        return render_template("update.html",result=res)

@app.route("/delete/<int:no>")
def delete(no):
    result=Todo.query.filter_by(id=no).first()
    db.session.delete(result)
    db.session.commit()
    return redirect("/")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password_=request.form.get("pass")
        c_pass=request.form.get("c_pass")
        number=request.form.get("mobile")
        if password_==c_pass:
            secure_password=password_
            # secure_password=sha256_crypt.encrypt(str(password_))
            # secure_password=sha256_crypt.hash(password_,secret)
            user=users(name=name,email=email,pwd=secure_password,mobile=number)
            db.session.add(user)
            db.session.commit()
            flash("Sucessfully Register !Now you can login!!",'grey lighten-1')
            return redirect(url_for("login"))
        else:
            flash("Password doesn't match!!",'red lighten-1')
            return redirect(url_for("register"))
    else:
        return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        pwd=request.form.get("pass")
        # flash(users().query.all())
        password_data=pwd
        # password_data=sha256_crypt.encrypt(str(pwd))
        # password_data=sha256_crypt.hash(pwd,secret)
        res=users.query.filter_by(email=email,pwd=password_data).first()
        if res:
            session['log']=email
            session['name']=res.name
            flash("Login Sucessfully!",'grey lighten-1')
            return redirect(url_for("home"))
        else:
            flash("Incorrect Credientials!",'red lighten-1')
            return redirect(url_for("login"))
    return render_template("login.html")
#         # usernamedata=db.execute("SELECT username from users WHERE username:=username",{"username":name}).fetchone()
#         # password_data=db.execute("SELECT password from users WHERE username:=username",{"username":name}).fetchone()
        
@app.route("/about")
def about():
    return render_template("about.html")    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))    

if __name__=="__main__":
    # db.create_all()
    app.run(debug=True,port=8080)

