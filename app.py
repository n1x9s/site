from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:15931@localhost/my_database'
db = SQLAlchemy(app)
Bootstrap(app)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pulse = db.Column(db.String(100), nullable=False)
    pressure = db.Column(db.String(500), nullable=False)


class RegistrationForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    pulse = IntegerField('Ваш пульс в данный момент', validators=[DataRequired()])
    pressure = FloatField(
        'Ваше давление в данный момент (верхнее и нижнее, где разделителем является точка. Например, 120.80).',
        validators=[DataRequired()])
    submit = SubmitField('Отправить')


name = Registration.name


@app.route('/')
def index():
    return render_template('index.html', title='Mental')


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        registration = Registration(name=form.name.data, pulse=form.pulse.data, pressure=form.pressure.data)
        db.session.add(registration)
        db.session.commit()
        flash('Registration data submitted successfully!')
        redirect('/show')
    return render_template('reg.html', form=form, title="Registration")


@app.route('/show', methods=['GET', 'POST'])
def show():
    form = RegistrationForm()
    if form.validate_on_submit():
        registration = Registration(name=form.name.data, pulse=form.pulse.data, pressure=form.pressure.data)
        db.session.add(registration)
        db.session.commit()
    return render_template('show.html', form=form, title="Show")


@app.route('/history', methods=['GET'])
def history():
    username = request.args.get('username')
    data = Registration.query.filter_by(name=username).all()  
    return render_template('history.html', data=data, title="History")


if __name__ == '__main__':
    app.run()
