from flask import Flask, render_template, request
import hashlib
import re
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class MyForm(FlaskForm):
    salt = StringField('Salt', validators=[DataRequired()])
    probability = FloatField('Probability', validators=[DataRequired(), NumberRange(min=0, max=1)])
    data = TextAreaField('Data', validators=[DataRequired()])


@app.route('/', methods=['GET'])
def index():
    form = MyForm()
    if 'salt' in request.args and 'probability' in request.args and 'data' in request.args:
        form.salt.data = request.args['salt']
        form.probability.data = float(request.args['probability'])
        form.data.data = request.args['data']
    elif form.validate():
        salt = form.salt.data
        probability = form.probability.data
        data = form.data.data
        table_data = [(email, branch_decision(email, salt, probability)) for email in split_multiline(data)]
        return render_template('results.html', table_data=table_data, form=form)
    return render_template('index.html', form=form)
# Client-provided function
def branch_decision(input_row: str, salt: str, probability: float):
    return (int(hashlib.md5((salt + input_row).encode("ascii")).hexdigest(), 16) / 2**128) < probability


# Function that splits the data content
def split_multiline(input_text):
    # Use regular expression to split the input using \n, \r\n, or \r as delimiters
    split_pattern = r'[\n\r\t\r\n]+'
    result = re.split(split_pattern, input_text)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)