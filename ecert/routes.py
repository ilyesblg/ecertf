import os
import json
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from ecert import app, db, bcrypt , mail
from ecert.forms import RegistrationForm, LoginForm, UpdateAccountForm , SurveyForm
from ecert.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required, login_manager , UserMixin
from flask_admin import Admin , AdminIndexView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func

posts = [
    {
        'author': 'https://www.ecert.tuntrust.tn',
        'title': 'Introduction ECERT',
        'content': 'ECERT est un portail qui vous permet de commander, de gérer et de révoquer les certificats électroniques de votre organisation à distance. Le portail se veut très simple d’utilisation. Ce manuel a pour objectif de vous guider dans l’utilisation du portail ecert.tuntrust.tn et de répondre aux éventuelles questions que vous pourriez vous poser au cours de son usage.',
        'date_posted': 'Aout 05, 2022'
    },
    {
        'author': 'https://www.ecert.tuntrust.tn',
        'title': 'Introduction de L\'Enquete',
        'content': 'Depuis l\'énquete en ligne, vous pouvez facilement Répondre à un sondage en ligne d\'opinion,pour nous aider à améliorer notre service',
        'date_posted': 'Aout 05, 2022'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role=False
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,urole=role)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)



@app.route("/survey", methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        avg=round((int(form.critere1.data)+int(form.critere2.data)+int(form.critere3.data)+int(form.critere4.data)+int(form.critere5.data)+int(form.critere6.data)+int(form.critere7.data)+int(form.critere8.data)+int(form.critere9.data)+int(form.critere10.data)+int(form.critere11.data))/11)
        post = Post(critere1=form.critere1.data,
                    critere2=form.critere2.data,
                    critere3=form.critere3.data,
                    critere4=form.critere4.data,
                    critere5=form.critere5.data,
                    critere6=form.critere6.data,
                    critere7=form.critere7.data,
                    critere8=form.critere8.data,
                    critere9=form.critere9.data,
                    critere10=form.critere10.data,
                    critere11=form.critere11.data,
                    opinion=form.opinion.data,
                    average=avg,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('Survey.html', title='ECERT - Enquête de satisfaction Client',
                           form=form, legend='ECERT - Enquête de satisfaction Client')




@app.route("/charts")
@login_required
def charts():
    if current_user.urole==True :
        avg_data1 = db.session.execute(Post.query.filter_by(average=1 ).statement.with_only_columns([func.count()]).order_by(None)).scalar()
        avg_data2 = db.session.execute(Post.query.filter_by(average=2 ).statement.with_only_columns([func.count()]).order_by(None)).scalar()
        avg_data3 = db.session.execute(Post.query.filter_by(average=3 ).statement.with_only_columns([func.count()]).order_by(None)).scalar()
        avg_data4 = db.session.execute(Post.query.filter_by(average=4 ).statement.with_only_columns([func.count()]).order_by(None)).scalar()
        dates = db.session.query(db.func.sum(Post.average), Post.date_posted).group_by(Post.date_posted).order_by(Post.date_posted).all()
        over_time_rate = []
        dates_label = []
        occ=[]
        for avg, date in dates:
            if (date.strftime("%m-%y") not in dates_label ):
                dates_label.append(date.strftime("%m-%y"))
                over_time_rate.append(avg)
                occ.append(1)
            else :
                over_time_rate[dates_label.index(date.strftime("%m-%y"))]+=avg
                occ[dates_label.index(date.strftime("%m-%y"))]+=1

        for i in range(len(occ)): 
            over_time_rate[i]=over_time_rate[i]/occ[i]
            
        return render_template('charts.html', title='Charts',
                                                        avrg_data1=avg_data1,
                                                        avrg_data2=avg_data2,
                                                        avrg_data3=avg_data3,
                                                        avrg_data4=avg_data4,
                                                        over_time_rate=json.dumps(over_time_rate),
                                                        dates_label =json.dumps(dates_label))
    else :
        flash('You Must be Admin', 'warning')
        return redirect(url_for('home'))
class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.urole==True :
            return (current_user.is_authenticated ) 
    def inaccessible_callback(self, name, **kwargs):
        flash('You Must be Admin', 'warning')
        return redirect(url_for('home'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.urole==True :
            return (current_user.is_authenticated )

    def inaccessible_callback(self, name, **kwargs):
        flash('You Must be Admin', 'warning')
        return redirect(url_for('home'))
admin=Admin(app , index_view=MyAdminIndexView())
admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Post,db.session))

