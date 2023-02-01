from time import sleep

import requests as r
from base64 import b64encode
from urllib.parse import unquote


class DiscordSession:
    """Create a discord session"""

    def __init__(self, token: str):

        self.token = token
        self.s = r.Session()
        self.s.headers['authorization'] = token
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                                       'AppleWebKit/537.36' \
                                       ' (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    def info(self) -> dict:
        """
        Get user info
        """
        return self.s.get('https://discord.com/api/v9/users/@me').json()

    def change_username(self,
                        new_username: str,
                        password: str):
        """
        Change Discord username
        :param new_username:
        :param password:
        :return:
        """
        return self.s.patch(f'https://discord.com/api/v9/users/@me', json={"username": new_username,
                                                                           "password": password}).json()

    def change_bio(self, new_bio: str) -> dict:
        """
        Change Discord user bio
        :param new_bio:
        :return:
        """
        return self.s.patch(f'https://discord.com/api/v9/users/@me', json={"bio": new_bio}).json()

    def change_avatar(self, image_url: str) -> dict:
        """
        Change Discord user avatar
        :param image_url:
        :return:
        """
        new_avatar = b64encode(r.get(image_url).content).decode("utf-8")
        _payload = {"avatar": f"data:image/png;base64,{new_avatar}"}
        return self.s.patch(f'https://discord.com/api/v9/users/@me', json=_payload).json()

    def friends_list(self) -> dict:
        """
        :return: dict with friends list
        """
        return self.s.get(f'https://discord.com/api/v9/users/@me/relationships').json()

    def guilds_list(self) -> dict:
        """
        :return: guilds dict
        """
        return self.s.get('https://discord.com/api/v9/users/@me/guilds').json()

    def guild_info(self, guild_id: int) -> dict:
        """
        :param guild_id:
        :return: info about guild
        """
        return self.s.get(f'https://discord.com/api/v9/guilds/{guild_id}').json()

    def get_roles(self, guild_id) -> dict:
        """
        :param guild_id:
        :return:
        """
        return self.s.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles').json()

    def guild_channels(self, guild_id: int) -> dict:
        """
        :param guild_id:
        :return: info about guild
        """
        return self.s.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels').json()

    def leave_guild(self, guild_id: int) -> r.request:
        """
        leave from guild
        :param guild_id:
        :return: request obj
        """
        return self.s.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', json={"lurking": False})

    def typing(self,
               channel_id: int,
               seconds: float = 0.5) -> r.request:
        """
        calls the "typing" method in channel
        :param channel_id:
        :param seconds: delay time
        :return:
        """
        response = self.s.post(f'https://discord.com/api/v9/channels/{channel_id}/typing')
        sleep(seconds)
        return response

    def send_message(self,
                     channel_id: int,
                     text_message: str) -> dict:
        """
        Send message to the channel
        :param channel_id:
        :param text_message:
        :return:
        """
        _data = {'content': text_message, 'tts': False}
        return self.s.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', json=_data).json()

    def reply_to_message(self,
                         guild_id: int,
                         channel_id: int,
                         message_id: int,
                         text_message: str):
        _payload = {
            "content": text_message,
            "tts": False,
            "message_reference": {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "message_id": message_id
            }
        }
        return self.s.post(f'https://discord.com//api/v9/channels/{channel_id}/messages', json=_payload).json()

    def get_history_by_channel_id(self,
                                  channel_id: int,
                                  messages_limit: int = 50) -> dict:
        """
        Get History by channel id
        :param channel_id:
        :param messages_limit: Number of messages in one request
        :return:
        """
        return self.s.get(
            f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={int(messages_limit)}').json()

    def get_history_by_user_id(self,
                               guild_id: int,
                               user_id: int,
                               offset: int = 0) -> dict:
        """
        get messages from user by ID
        :param guild_id:
        :param user_id:
        :param offset: offset number of messages from the last message
        :return:
        """
        response = self.s.get(
            f"https://discord.com/api/v9/guilds/{guild_id}/messages/search?author_id={user_id}&offset={offset}"
        )
        return response.json()

    def react_on_message(self,
                         channel_id: int,
                         message_id: int,
                         react: str = '🎉') -> dict:
        """
        Reaction on message
        :param channel_id:
        :param message_id:
        :param react:
        :return:
        """
        response = self.s.put(
            f'https://discord.com/api/v9/channels/{channel_id}/messages/{str(message_id)}/reactions/{react}/@me')
        try:
            return {"status": response,
                    "username": self.info()['username'],
                    "react": unquote(react)}
        except KeyError:
            return {"status": self.info(),
                    "token": self.token}

    def delete_react_from_message(self,
                                  channel_id: int,
                                  message_id: int,
                                  react: str = '🎉') -> dict:
        """
        Delete reaction from message by message_id
        :param channel_id:
        :param message_id:
        :param react:
        :return:
        """
        response = self.s.delete(
            f'https://discord.com/api/v9/channels/{channel_id}/messages/{str(message_id)}/reactions/{react}/@me')
        try:
            return {"status": response.status_code,
                    "username": self.info()['username'],
                    "react": unquote(react)}
        except KeyError:
            return {"status": response.status_code,
                    "token": self.token}

    def delete_message_by_id(self,
                             channel_id: int,
                             message_id: int) -> int:
        """
        Delete message
        :param channel_id:
        :param message_id:
        :return:
        """
        return self.s.delete(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}').status_code

    def delete_channel_by_id(self, channel_id) -> int:
        """
        :param channel_id:
        :return:
        """
        return self.s.delete(f'https://discord.com/api/v9/channels/{channel_id}').status_code
