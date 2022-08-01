import time
import requests as r

class DiscordSession:

    """Create a discord session"""
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = str(chat_id)
        self.s = r.Session()
        self.s.headers['authorization'] = token
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
                                       ' (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'


    def typing(self, sec=float(0.5)):
        self.s.post(f'https://discord.com/api/v9/channels/{self.chat_id}/typing')
        time.sleep(sec)

    def send_msg(self, message):
        _data = {'content': message, 'tts': False}
        self.s.post(f'https://discord.com//api/v9/channels/{self.chat_id}/messages', json=_data).json()

    def get_history(self, messages_limit):
        response = self.s.get(f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit={str(messages_limit)}')
        return response

    def react_on_message(self, message_id, react='🎉'):
        self.s.put(f'https://discord.com/api/v9/channels/{self.chat_id}/messages/{str(message_id)}/reactions/{react}/@me')

    def delete_react_from_message(self, message_id, react='🎉'):
        self.s.delete(f'https://discord.com/api/v9/channels/{self.chat_id}/messages/{str(message_id)}/reactions/{react}/@me')
