from flask import Flask, render_template, redirect, url_for
import hashlib
import re
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


class MyForm(FlaskForm):
    salt = StringField('Salt', validators=[DataRequired()])
    probability = FloatField('Probability', validators=[DataRequired(), NumberRange(min=0, max=1)])
    data = TextAreaField('Data', validators=[DataRequired()])


class Usage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salt = db.Column(db.String(50), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    data = db.Column(db.Text, nullable=False)
    table_html = db.Column(db.Text, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.is_submitted():
        salt = form.salt.data
        probability = form.probability.data
        data = form.data.data
        table_data = [(email, branch_decision(email, salt, probability)) for email in split_multiline(data)]
        table_html = '<table><thead><tr><th>Inputs</th><th>Outputs</th></tr></thead><tbody>'
        for row in table_data:
            table_html += f'<tr><td>{row[0]}</td><td>{row[1]}</td></tr>'
        table_html += '</tbody></table>'
        usage = Usage(salt=salt, probability=probability, data=data, table_html=table_html)
        db.session.add(usage)
        db.session.commit()
        return redirect(url_for('results'))
    return render_template('index.html', form=form)


@app.route('/results')
def results():
    usage = Usage.query.order_by(Usage.id.desc()).first()
    if usage:
        table_html = usage.table_html
    else:
        table_html = ''
    form = MyForm()
    return render_template('results.html', usage=usage, table_html=table_html, form=form)


# Client-provided function
def branch_decision(input_row: str, salt: str, probability: float):
    return (int(hashlib.md5((salt + input_row).encode("ascii")).hexdigest(), 16) / 2**128) < probability


# Function that splits the data content
def split_multiline(input_text):
    # Use regular expression to split the input using \n, \r\n, or \r as delimiters
    split_pattern = r'[\n\r\t\r\n]+'
    result = re.split(split_pattern, input_text)

    # Remove any leading or trailing whitespace from each element in the list
    result = [item.strip() for item in result]

    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)