import os
import telegram
import openai
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

openai_api_key = os.getenv('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')

bot = telegram.Bot(token=telegram_bot_token)
openai.api_key = openai_api_key

def generate_text(prompt):
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def handle_message(update, context):
    message = update.message.text
    if message.startswith('/start'):
        bot.send_message(chat_id=update.effective_chat.id, text='Hello! Send me a prompt and I will generate a text for you.')
    else:
        generated_text = generate_text(message)
        bot.send_message(chat_id=update.effective_chat.id, text=generated_text)

if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, Filters

    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
