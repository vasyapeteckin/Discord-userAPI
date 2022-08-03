from time import sleep
import requests as r
from base64 import b64encode


class DiscordSession:
    """Create a discord session"""

    def __init__(self, token):
        self.token = token
        self.s = r.Session()
        self.s.headers['authorization'] = token
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                                       'AppleWebKit/537.36' \
                                       ' (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    def info(self):
        # Get user info by token
        return self.s.get('https://discord.com/api/v9/users/@me').json()

    def change_username(self, new_username, password):
        # Change Discord username
        return self.s.patch(f'https://discord.com/api/v9/users/@me', json={"username": new_username,
                                                                           "password": password}).json()

    def change_bio(self, new_bio):
        # Change Discord user bio
        return self.s.patch(f'https://discord.com/api/v9/users/@me', json={"bio": new_bio}).json()

    def change_avatar(self, image_url):
        # Change Discord user avatar
        new_avatar = b64encode(r.get(image_url).content).decode("utf-8")
        _payload = {"avatar": f"data:image/png;base64,{new_avatar}"}
        return self.s.patch(f'https://discord.com/api/v9/users/@me', json=_payload).json()

    def friends_list(self):
        # Return friends list
        return self.s.get(f'https://discord.com/api/v9/users/@me/relationships').json()

    def guilds_list(self):
        # return guilds list
        return self.s.get('https://discord.com/api/v9/users/@me/guilds').json()

    def guild_info(self, guild_id):
        # return info about guild
        return self.s.get(f'https://discord.com/api/v9/guilds/{guild_id}').json()

    def guild_channels(self, guild_id):
        # return info about guild
        return self.s.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels').json()

    def leave_guild(self, guild_id):
        # leave from guild
        return self.s.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', json={"lurking": False})

    def typing(self, channel_id, seconds=float(0.5)):
        # Call typing function
        if type(seconds) == float or type(seconds) == int:
            response = self.s.post(f'https://discord.com/api/v9/channels/{channel_id}/typing')
            sleep(seconds)
            return response
        else:
            response = self.s.post(f'https://discord.com/api/v9/channels/{channel_id}/typing')
            sleep(0.5)
            return response

    def send_message(self, channel_id, text_message):
        # Send message
        _data = {'content': text_message, 'tts': False}
        return self.s.post(f'https://discord.com//api/v9/channels/{channel_id}/messages', json=_data).json()

    def reply_to_message_by_id(self, guild_id, channel_id, message_id, text_message):
        _data = {
                  "content": text_message,
                  "tts": False,
                  "message_reference": {
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "message_id": message_id
                  }
                }
        return self.s.post(f'https://discord.com//api/v9/channels/{channel_id}/messages', json=_data).json()

    def get_history_by_channel_id(self, channel_id, messages_limit: int = 50):
        # Get History by channel id
        return self.s.get(
            f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={int(messages_limit)}').json()

    def get_history_by_user_id(self, guilds_id, user_id, offset=0):
        # get last 25 messages from user by ID
        response = self.s.get(
            f"https://discord.com/api/v9/guilds/{guilds_id}/messages/search?author_id={user_id}&offset={int(offset)}"
        )
        # TODO: Get all history by user_id
        return response.json()

        # TODO: Combine methods PUT/DELETE
    def react_on_message(self, channel_id, message_id, react='🎉'):
        # Reaction on message by message_id
        response = self.s.put(
            f'https://discord.com/api/v9/channels/{channel_id}/messages/{str(message_id)}/reactions/{react}/@me')
        try:
            return {"status": response, "username": self.info()['username'], "react": react}
        except KeyError:
            return {"status": self.info(), "token": self.token}

    def delete_react_from_message(self, channel_id, message_id, react='🎉'):
        # Delete reaction from message by message_id
        response = self.s.delete(
            f'https://discord.com/api/v9/channels/{channel_id}/messages/{str(message_id)}/reactions/{react}/@me')
        try:
            return {"status": response, "username": self.info()['username'], "react": react}
        except KeyError:
            return {"status": self.info(), "token": self.token}

    def delete_message_by_id(self, channel_id, message_id):
        # Delete message by message id
        return self.s.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}')
