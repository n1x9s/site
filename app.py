from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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
    pulse = StringField('Ваш пульс в данный момент', validators=[DataRequired()])
    pressure = StringField('Ваше давление в данный момент', validators=[DataRequired()])
    submit = SubmitField('Отправить')


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
    return render_template('reg.html', form=form, title="Registration")


if __name__ == '__main__':
    app.run()
