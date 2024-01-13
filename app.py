from flask import Flask, request, jsonify
import difflib

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

def get_closest_match(query, responses):
    closest_match = difflib.get_close_matches(query, responses.keys(), n=1, cutoff=0.5)
    return responses.get(closest_match[0]) if closest_match else None

def get_reply(message, responses):
    question = message.lower()
    reply = responses.get(question)

    if not reply:
        closest_match_reply = get_closest_match(question, responses)
        return closest_match_reply if closest_match_reply else 'Anlamsız bir soru sordun.'
    
    return reply

@app.route('/apis/chatbotapiv1/message=<message>', methods=['GET'])
def get_response(message):
    responses = load_responses()
    reply = get_reply(message, responses)
    return jsonify({'received': message, 'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
