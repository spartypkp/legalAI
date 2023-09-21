from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Data that you want to display on the webpage
    page_title = "Dynamic Webpage"
    content_text = "This content is generated dynamically with Python and Flask."
    footer_text = "© 2023 Your Website"
    
    return render_template('index.html', title=page_title, content=content_text, footer=footer_text)

if __name__ == '__main__':
    app.run(debug=True)
