from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Cafe Location on Google Maps URL', validators=[DataRequired(), URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 8PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=["", "☕", "☕☕", "☕☕☕", "☕☕☕☕",
                                                                                       "☕☕☕☕☕"])
    wifi_rating = SelectField('WIFI Rating', validators=[DataRequired()], choices=["", "✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪",
                                                                                   "💪💪💪💪💪"])
    power_outlet_rating = SelectField('Power Outlet Rating', validators=[DataRequired()], choices=["", "✘", "🔌", "🔌🔌",
                                                                                                   "🔌🔌🔌", "🔌🔌🔌🔌",
                                                                                                   "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', "a", encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.cafe.data},{form.location_url.data},{form.opening_time.data},"
                           f"{form.closing_time.data},{form.coffee_rating.data},{form.wifi_rating.data},"
                           f"{form.power_outlet_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
