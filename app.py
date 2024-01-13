from flask import Flask, request, jsonify, render_template
import json
from fuzzywuzzy import fuzz

app = Flask(__name__)

def load_responses():
    responses = {}
    with open('sc.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(':')
            if len(parts) == 2:
                question, answer = parts[0].lower(), parts[1]
                responses[question] = answer
    return responses

def write_responses(responses):
    with open('sc.txt', 'w', encoding='utf-8') as file:
        for question, answer in responses.items():
            file.write(f"{question}:{answer}\n")

def get_closest_match(query, responses):
    closest_match = max(responses.keys(), key=lambda k: fuzz.ratio(query, k))
    return closest_match

def get_reply(message, responses):
    question = message.lower()

    closest_match = get_closest_match(question, responses)
    closest_match_reply = responses.get(closest_match)
    
    return closest_match_reply

@app.route('/apis/chatbotapiv1/message=<message>', methods=['GET'])
def get_response(message):
    responses = load_responses()
    reply = get_reply(message, responses)
    response_json = json.dumps({'alındı': message, 'cevap': reply.replace('\n', ' ').replace('\r', '').replace('\t', '').replace('\xa0', '').strip()}, ensure_ascii=False)
    return response_json, 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/mamimod', methods=['GET', 'POST'])
def mamimod():
    if request.method == 'POST':
        new_content = request.form['new_content']
        updated_responses = {}
        for line in new_content.split('\n'):
            parts = line.strip().split(':')
            if len(parts) == 2:
                question, answer = parts[0].lower(), parts[1]
                updated_responses[question] = answer
        write_responses(updated_responses)

    current_content = '\n'.join([f"{question}:{answer}" for question, answer in load_responses().items()])
    return render_template('mamimod.html', current_content=current_content)

if __name__ == '__main__':
    app.run(debug=True)
