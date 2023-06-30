from flask import Flask, render_template

app = Flask(__name__, template_folder = 'templates')

@app.route("/")
def home():
    return render_template('index.html')
    
# @app.route('/admin')
# def index():
#     return render_template('template.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/parameter')
def parameter():
    return render_template('parameter.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

if __name__ == "__main__":
    app.run(debug=True)
