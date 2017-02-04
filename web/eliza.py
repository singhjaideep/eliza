from flask import Flask, request
import telepot
import urllib3
import config
from nltk.chat.eliza import eliza_chatbot

#Server stuff
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

#Bot stuff
secret = config.secret
bot = telepot.Bot(config.bot)
bot.setWebhook("https://jdsir.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        if text == "/start":
            bot.sendMessage(chat_id, "Hello, I'm Liza the therapist.  How can I help?")
        else:
            bot.sendMessage(chat_id, eliza_chatbot.respond(text))
    return "OK"

@app.route('/')
def hello_world():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')