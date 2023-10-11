import hashlib
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        salt = request.form.get('salt')
        input_row = request.form.get('input')  # Correct the field name here
        probability = float(request.form.get('probability'))
        # Do something with the form data (e.g., print it)
        list1 = data_split(input_row)
        list2 = [branch_decision(row, salt, probability) for row in list1]
        print(list1, list2)

        return render_template('results.html', list1=list1, list2=list2, salt=salt, probability=probability)
    
    return render_template('index.html', css=url_for('static', filename='styles.css'))


# Client-provided function
def branch_decision(input_row: str, salt: str, probability: int):
    return (int(hashlib.md5((salt + input_row).encode("ascii")).hexdigest(), 16) / 2**128) < probability


# Function that splits the data content
def data_split(text):
    list1 = []
    word  = ''
    for i in text:
        if i in ['\n', '\t', '\r', '\r\n']:
            if len(word) > 0:
                list1 += [word]
                word = ''
        else:
            word += i
    return list1



if __name__ == '__main__':
    app.run(debug=True)