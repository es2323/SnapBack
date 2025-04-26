from flask import Flask, render_template
from routes.main import main
app.register_blueprint(main)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # loads /templates/index.html

if __name__ == '__main__':
    app.run(debug=True)
