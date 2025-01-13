import json
import os
import time
# DEBUG:
import tracemalloc
from datetime import datetime

from rich import print as pprint
from telethon import TelegramClient, utils, functions
from telethon.errors import SessionPasswordNeededError, rpcerrorlist
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)

tracemalloc.start()
######################

_statix = {
    'bot_K':'',
    'test': '',
    'prod': '',
    'id': '',
    'hash': '',
    'uname':'',
    'phone':'',
    'chan': '',
}

pprint('[*]', os.getcwd())
start = time.time()

with TelegramClient(api_id=_statix['id'],
                    api_hash=_statix['hash'],
                    session='./session.data',
                    ) as client:
    counter = 0


    async def main(phone: str, limit: int):
        user_input_chan = input('Enter entity URL or entity ID):')

        me = await client.get_me()

        print('\n', me, utils.get_display_name(me), '\n')

        if user_input_chan.isdigit():
            ent = PeerChannel(int(user_input_chan))
        else:
            ent = user_input_chan

        my_chan = await client.get_input_entity(ent)
        chan = await my_chan.get_entity()
        print(chan)
        client(functions.channels.JoinChannelRequest(my_chan))

        print('[*] CHANNEL ID :', my_chan.channel_id)
        return 0
        await client.start()
        print('[*] Client Created.')

        # Auth Check:
        if not client.is_user_authorized:
            try:
                await client.sign_in(phone)
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))
        result = await client(functions.account.SetContentSettingsRequest(sensitive_enabled=True))
        pprint('RESULT:', result)

    _MAX_ = int(input('GIVE THE MAX MSG ID:'))
    assert isinstance(_MAX_, int)
    client.loop.run_until_complete(main(_statix['phone'], _MAX_))

end = time.time()
dif = end - start
print(f'Time : {dif:.2f}')