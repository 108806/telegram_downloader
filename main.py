import json
import os
import time

import downloader
# DEBUG:
import tracemalloc
from datetime import datetime

from rich import print as pprint
from telethon import TelegramClient, utils
from telethon.errors import SessionPasswordNeededError

from dotenv import load_dotenv
tracemalloc.start()

######################
load_dotenv()
api_id = int(os.getenv('id').strip())
api_hash = os.getenv('hash')
phone = os.getenv('phone')
channel = os.getenv('chan')
print(f"API ID: {api_id}")
print(f"API Hash: {api_hash}")
print(f"Phone: {phone}")

_statix = {
    "id": api_id,  # API ID for user account
    "hash": api_hash,  # API Hash for user account
    "phone": phone,  # Your phone number
    "chan": 0,  # Channel to interact with:
    #String: Assumes a username, phone number, or invite link.
    #Integer: Assumes a user ID, group ID, or channel ID, THAT IS NOT WORKING NOW.
}

pprint("[*]", os.getcwd())
start = time.time()

if not _statix['chan']:
    ctx = str(input('Provide the target channel:'))
    if ctx.isnumeric():
        _statix['chan'] = int(ctx)
    else:
        _statix['chan'] = ctx


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


# Initialize the Telegram Client for user account
with TelegramClient(
    session="./session.ghst.session",
    api_id=_statix["id"],
    api_hash=_statix["hash"]
) as client:
    async def main():
        me = await client.get_me()
        pprint(me)
        print(utils.get_display_name(me))
        # Start client and authenticate
        await client.start()
        if not await client.is_user_authorized():
            try:
                await client.sign_in(_statix["phone"])
                code = input("Enter the login code sent to your Telegram account: ")
                await client.sign_in(code=code)
            except SessionPasswordNeededError:
                password = input("Enter your 2FA password: ")
                await client.sign_in(password=password)

        # Print user info
        me = await client.get_me()
        pprint(f"Logged in as: {me.username or me.first_name}")

        # Interact with a channel
        my_chan = await client.get_entity(_statix["chan"])
        pprint(f"Channel info: {my_chan.title} (ID: {my_chan})")

        latest_message = await client.get_messages(my_chan, limit=1)
        if latest_message:
            max_id = latest_message[0].id
            print(f"Max Post ID: {max_id}")

        await downloader.Start(client, my_chan)

    client.loop.run_until_complete(main())

end = time.time()
dif = end - start
print(f"Time: {dif:.2f} seconds")




