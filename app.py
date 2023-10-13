from flask import Flask, render_template, request, url_for, Response, redirect
import hashlib
import re

app = Flask(__name__)


# Create a new route to generate the static HTML page and display it
@app.route('/generate_static_html', methods=['POST'])
def generate_static_html():
    if request.method == 'POST':
        salt = request.form.get('salt')
        probability = request.form.get('probability')
        list1 = request.form.get('list1').split('\n')  # Split list1 by line breaks
        list2 = request.form.get('list2').split('\n')  # Split list2 by line breaks

        # Create the HTML content for the static page with the table structure
        static_html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                table {{
                    width: 70%;
                    margin: 0 auto;
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid black;
                }}
            </style>
        </head>
        <body>
            <h1>Results</h1>
            <h2>Salt: {salt}</h2>
            <h2>Probability: {probability}</h2>
            <table>
                <tr>
                    <th>Inputs</th>
                    <th>Outputs</th>
                </tr>
                {"".join(f"<tr><td>{list1[i]}</td><td>{list2[i]}</td></tr>" for i in range(len(list1)))}
            </table>
        </body>
        </html>
        """

        return static_html_content

 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        salt = request.form.get('salt')
        input_row = request.form.get('input')
        probability = float(request.form.get('probability'))
        list1 = split_multiline_input(input_row)
        list2 = [branch_decision(row, salt, probability) for row in list1]

        # Use redirect to change the URL to '/results1.html' when displaying results
        return redirect(url_for('results', salt=salt, probability=probability, list1=list1, list2=list2))

    return render_template('index.html', css=url_for('static', filename='styles.css'))


# Client-provided function
def branch_decision(input_row: str, salt: str, probability: int):
    return (int(hashlib.md5((salt + input_row).encode("ascii")).hexdigest(), 16) / 2**128) < probability


# Function that splits the data content
def split_multiline_input(input_text):
    # Use regular expression to split the input using \n, \r\n, or \r as delimiters
    split_pattern = r'[\n\r\t\r\n]+'
    result = re.split(split_pattern, input_text)

    # Remove any leading or trailing whitespace from each element in the list
    result = [item.strip() for item in result]

    return result


# Define a new route for the results page
@app.route('/results.html')
def results():
    salt = request.args.get('salt')
    probability = float(request.args.get('probability'))
    list1 = request.args.getlist('list1')
    list2 = request.args.getlist('list2')

    return render_template('results.html', list1=list1, list2=list2, salt=salt, probability=probability)

# ...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)