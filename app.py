from flask import Flask, request, jsonify, render_template
import re
import long_responses as long

app = Flask(__name__)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
    percentage = float(message_certainty) / float(len(recognised_words))
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    return int(percentage * 100) if has_required_words or single_response else 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'sup', 'hey'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    return check_all_messages(split_message)

# 👇 This renders the frontend
@app.route("/")
def home():
    return render_template("index.html")

# 👇 This handles chat requests from frontend JS
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
