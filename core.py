from telebot import types
from app import App

START = 'start' # check for subscription
MAIN = 'main'
PHONE = 'phone'
STOP = 'stop'


class Core(App):

    def __init__(self):
        super().__init__()
        self._client_state = {}

    def register_handlers(self):
        @self.bot.message_handler(commands=['check'])
        def check_subscription(message):
            chat_id = message.chat.id
            channel = self._conf["bot"]["channel"]
            self.bot.send_message(chat_id,f"trying to reach {channel}")
            try:
                member = self.bot.get_chat_member(channel, chat_id)
                if member.status in ['member','administrator', 'creator']:
                    self.bot.send_message(chat_id, f"You have been subscribed to the channel {member.status} {member.is_member}")
                else:
                    self.bot.send_message(chat_id, f"You have not been subscribed to the channel {member.status} {member.is_member}")
            except Exception as e:
                self.bot.send_message(chat_id, f"Error: {e}")


        @self.bot.message_handler(commands=['replenish'])
        def clear_keyboard(message: types.Message) -> None:
            # Create a ReplyKeyboardRemove object
            remove_markup = types.ReplyKeyboardRemove()
            # Send a message with the ReplyKeyboardRemove markup to clear the keyboard
            self.bot.send_message(message.chat.id,
                                  self._conf["bot"]["start"].format(name=message.chat.first_name,
                                                                    last_name=message.chat.last_name),
                                  reply_markup=remove_markup)


        @self.bot.message_handler(commands=['start', 'help'])
        def start(message):
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton('Go to chat ', url="https://t.me/intelgdx")
            button2 = types.InlineKeyboardButton('Button 2', callback_data='button2')
            # Add buttons to the markup
            markup.add(button1, button2)

            # Send the message with the inline keyboard
            self.bot.send_message(message.chat.id, "Choose an option to replenish your account:", reply_markup=markup)

        @self.bot.message_handler(commands=['info'])
        def info_start(message):
            markup = types.ReplyKeyboardMarkup(row_width=2)
            button1 = types.KeyboardButton('Button 1')
            button2 = types.KeyboardButton('Button 2')
            # Add buttons to the markup
            markup.add(button1, button2)

            # Send the message with the inline keyboard
            self.bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text in ['Button 1', 'Button 2'])
        def handle_button(message):
            if message.text == 'Button 1':
                self.bot.reply_to(message, "You pressed Button 1")
            elif message.text == 'Button 2':
                self.bot.reply_to(message, "You pressed Button 2")

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == "button1":
                self.bot.send_message(call.message.chat.id, "Button 1")
                self.bot.answer_callback_query(call.id)
            elif call.data == "button2":
                self.bot.answer_callback_query(call.id, "You clicked Button 2", show_alert=True)

        @self.bot.inline_handler(lambda query: query.query == 'text')
        def query_text(inline_query):
            try:
                r = types.InlineQueryResultArticle('1', 'Result',
                                                   types.InputTextMessageContent('Result message.'))
                r2 = types.InlineQueryResultArticle('2', 'Result2',
                                                    types.InputTextMessageContent('Result message2.'))
                self.bot.answer_inline_query(inline_query.id, [r, r2])
            except Exception as e:
                print(e)
