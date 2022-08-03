from DiscordAPI import DiscordSession

token = "YOUR_DISCORD_TOKEN"
guild_id = "guild_id_where_to_look_for_messages"


def delete_last_25_messages():
    user = DiscordSession(token)
    user_id = user.info()['id']

    messages_list = user.get_history_by_user_id(guild_id, user_id)['messages']
    for message in messages_list:
        user.delete_message_by_id(message[0]['channel_id'], message[0]['id'])


delete_last_25_messages()
