# from doctest import debug
import email
from email.policy import default
from enum import unique
from turtle import title
from flask import Flask, flash, render_template, url_for,flash,redirect,request
import requests
# from flask import request, url_for
from flask_sqlalchemy import  SQLAlchemy
# from requests import request
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from forms import RegistrationForm,LoginForm
from datetime import datetime
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash,check_password_hash
from flask_api import status

# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
Bootstrap(app)



# db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Anishad@123@localhost/flaskproject'
app.config["SECRET_KEY"]="IMAPROGRAMERALSOMATHMATACIANPHYSICIST"





db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(55),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    passsword = db.Column(db.String(500),nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class MobileNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_number = db.Column(db.String(100),nullable=False)
    zone = db.Column(db.String(100),nullable=False)
    customer_call_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    # def __repr__(self):
    #     return f"User('{self.customer_number}','{self.zone}',,'{self.customer_call_time}')"


class TotalGift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gift = db.Column(db.String(100),nullable=False)
    gift_qantity = db.Column(db.String(100),nullable=False)
    # customer_call_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.gift}','{self.gift_qantity}',)"

class PreviousMobileNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MobileNumber = db.Column(db.String(100),nullable=False)
    # gift_qantity = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"PreviousMobileNumbers('{self.MobileNumber}',)"

class DATA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.String(100),nullable=False)
    ChannellD = db.Column(db.String(100),nullable=False)
    circle = db.Column(db.String(100),nullable=False)
    operator = db.Column(db.String(100),nullable=False)
    datetim  = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.who}','{self.ChannellD}','{self.circle}','{self.operator}','{self.datetim}')"


@app.route("/sendmissedcalldetails",methods=["POST"])
# @login_required
def send_missed_call_details():
    dic = {}
    if request.method== "POST":
        print("Hiiii___________________________________________________________")
        who = request.args.get("who")
        print(who)
        ChannellD = request.args.get("ChannelID")
        circle = request.args.get("Circle")
        operator = request.args.get("Operator") 
        datetim = request.args.get("DateTime")
        print(who,ChannellD,circle,operator,datetim,"11"*25)
        # try:
        me = DATA(who=str(who),ChannellD=str(ChannellD),circle=str(circle),operator=str(operator),datetim=str(datetim))
        db.session.add(me)
        db.session.commit()
        yourapicode = ""
        TESTIN = ""
        channl = "2"
        DCS = "0"
        flashsms = "0"
        number = ""
        textmessage = ""
        route = "1"
        register_entity_id = ""
        register_dlt_id = ""
        veribale = requests.get(f"""https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={yourapicode}&senderid={TESTIN}&channel={channl}&DCS={DCS}&flashsms={flashsms}&number={number}&text={textmessage}&route={route}&EntityId={register_entity_id}&dlttemplateid={register_dlt_id}""")
        return veribale.text

        # except:
        # # db.session.add(me)
        # # db.session.commit()
        #  return status 
    

@app.route("/")
@login_required
def Dash_Board():
    page = request.args.get("page",1,type=int)
    # data = MobileNumber.query.order_by(MobileNumber.customer_call_time.desc())
    data = MobileNumber.query.paginate(page=page,per_page=2)
    return render_template('totalmobile.html',data=data)


@app.route("/totalgift")
@login_required
def Totalgift():
    data = TotalGift.query.all()
    return render_template('totalgift.html',data=data)




@app.route("/zonewisenumber")
@login_required
def Zonewisenumber():
    data = MobileNumber.query.filter_by(zone="9322014967").all()
    return render_template('totalmobile.html',data=data)


@app.route("/login",methods = ["POST","GET"])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # return redirect(url_for("Dash_Board"))
    #     print(user,"3"*50)
        if user: 
    #         # print(form.password.data)
    #         # print(user.passsword)
            # print("sha256$2pi8BpnTQXhTFALg$d0453a9b331fed69c01a7ef1c5d1acf683125cb0258265afaf4e61ba8456898f")
    #         return redirect(url_for("Dash_Board"))
            if check_password_hash(user.passsword,form.password.data):
                login_user(user,remember=form.remember.data)
            # print(user.passsword)
            # if user.passsword == form.password.data:
                # print("sha256$2pi8BpnTQXhTFALg$d0453a9b331fed69c01a7ef1c5d1acf683125cb0258265afaf4e61ba8456898f")

                return redirect(url_for("Dash_Board"))
    #     # newuser = 
    #     print(form.email.data,"------------------------------------")
    return render_template('login.html',title = "Login",form=form)


@app.route("/register",methods = ["POST","GET"])
def Register():
    form  = RegistrationForm()
    # if request.method== "POST"
    # print(form.email.data,"-----1111111111111111111---",form.username.data,form.password.data)
    if form.validate_on_submit():
        # print(hello)
        # print(form.email.data,"------------------------------------",form.username.data,form.password.data)
        hassed_passward = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,email=form.email.data,passsword=hassed_passward)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("Dash_Board"))
        # flash(f"accont create for {form.username.data}!")
        # return redirect(url_for("Login"))
    return render_template('register.html',title="Registraion",form=form)


@app.route('/logout',methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You have Been Out Thanks")
    return redirect(url_for("Login"))


if __name__ == "__main__":
    app.run(debug=True,)
