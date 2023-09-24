from flask import Flask, render_template, stream_with_context, Response, request, jsonify
from flask_cors import CORS  # You'll need to install this module: pip install Flask-CORS
import json
import createAbe
CURRENT_ANSWER = ["","",""]
app = Flask(__name__)
CORS(app)  # Allows all domains (not safe for production)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/playground')
def playground():
    return render_template('playground.html')

@app.route('/ask_ai', methods=['GET','POST'])
def ask_ai():
    question = request.get_json()['question']
    
    # This is a mockup. Replace this with code that sends the question to your model.
    # For example, call createAbe.ask_abe() here without streaming.
    # Just get the answer and return it.
    # Store the result somewhere for the next request to pick it up.
    
    final_answer, citations = createAbe.ask_abe(question, False, False, True)
    CURRENT_ANSWER = [final_answer, citations]
    
    return jsonify({'final_answer': final_answer, 'citations': citations})

'''
@app.route('/ask_ai_stream', methods=['GET'])
@stream_with_context
def ask_ai_stream():
    # Here, instead of getting the question again, you'll fetch the previously stored result
    # and stream it back.
    # Modify as needed for your logic.
    template = CURRENT_ANSWER[0]
    documentation = CURRENT_ANSWER[1]
    question = CURRENT_ANSWER[2]

    def generate(template, documentation, question):
        for message in createAbe.stream_answer(template, documentation, question):  # This is a mockup. Replace with the right logic.
            yield f"data: {message}\n\n"
            
    return Response(generate(template, documentation, question), mimetype="text/event-stream")
'''

if __name__ == "__main__":
    app.run(debug=True)
