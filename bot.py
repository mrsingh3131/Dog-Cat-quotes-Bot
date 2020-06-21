from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if 'dog' in incoming_msg:
        # return a dog pic
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        data = r.json()
        message = data["message"]
        msg.media(message)
        responded = True
    if not responded:
        msg.body('I know about famous dogs, cats and quotes only sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()