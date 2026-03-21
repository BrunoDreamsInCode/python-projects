from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv, pprint


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Converts a SelectField value into its display label (emoji) for CSV storage
def get_label_from_field(field):
    for value, label in field.choices:
        if value == field.data:
            return label

# Get all fiends from web form, and add to a CSV file.
def add_data_form(form):
    #FILDNAMES FROM CSV FILE
    fieldnames = ['Cafe Name', 'Location', 'Open', 'Close', 'Coffee', 'Wifi', 'Power']

    #ADDING DATA TO A CSV FILE
    with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writerow({
            'Cafe Name': form.cafe_name.data,
            'Location': form.location.data,
            'Open': form.open_time.data,
            'Close': form.closing_time.data,
            'Coffee': get_label_from_field(form.cafe),  # Converts a SelectField value into its display label (emoji) for CSV storage
            "Wifi": get_label_from_field(form.wifi_rating), # Converts a SelectField value into its display label (emoji) for CSV storage
            "Power": get_label_from_field(form.power_outlet_rating), # Converts a SelectField value into its display label (emoji) for CSV storage
        })

# Form to collect cafe information including location, hours, and ratings
class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location on Google Maps', validators=[DataRequired()])
    open_time = StringField('Open Time e.g: 5AM', validators=[DataRequired()])
    closing_time = StringField('Close e.g: 11PM', validators=[DataRequired()])
    cafe = SelectField(label='Coffee', choices=[
                                                    ('0','❌'),
                                                    ('1', '☕'),
                                                    ('2', '☕☕'),
                                                    ('3', '☕☕☕'),
                                                    ('4', '☕☕☕☕'),
                                                    ('5', '☕☕☕☕☕'),
                                                ],validators=[DataRequired()])
    wifi_rating = SelectField('Wifi', choices=[
                                                        ('0', '❌'),
                                                        ('1', '💪'),
                                                        ('2', '💪💪'),
                                                        ('3', '💪💪💪'),
                                                        ('4', '💪💪💪💪'),
                                                        ('5', '💪💪💪💪💪'),
                                                    ], validators=[DataRequired()])
    power_outlet_rating = SelectField('Power', choices=[
                                                                ('0','❌'),
                                                                ('1', '🔌'),
                                                                ('2', '🔌🔌'),
                                                                ('3', '🔌🔌🔌'),
                                                                ('4', '🔌🔌🔌🔌'),
                                                                ('5', '🔌🔌🔌🔌🔌'),
                                                            ],validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        #DEBUG -- PRINT ALL DATA FROM FORM
        print("True")
        add_data_form(form)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        pprint.pprint(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)



if __name__ == '__main__':
    app.run(debug=True)



