import time
from termcolor import colored
import colorama
import json
import asyncio
from telethon.sync import TelegramClient, events
from telethon.tl import types
import re

colorama.init()

print(colored("Telegram Promo Bot", "cyan"))
print("\nBy: ")
print(colored("\tZile42O", "light_green"))
print("\n\n")

try:
	with open('accounts.json', 'r', encoding='utf-8') as file:
		accounts = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
	print(colored("Unable to load accounts.json", "red"))
	exit

print(colored("Accounts loaded, starting..", "cyan"))
time.sleep(2)

async def send_promo_messages(client, account):
	dialogs = await client.get_dialogs()
	while True:
		count_groups = 0
		count_messages = 0
		count_fail_messages = 0
		for dialog in dialogs:
			if dialog.is_group:
				count_groups += 1
				try:
					if account["forward_message"] != '':
						match = re.match(r'https://t.me/s/([^/]+)/(\d+)', account["forward_message"])
						if match:
							match_group_id = match.group(1)
							message_id = int(match.group(2))					
							messages = await client.get_messages(match_group_id, ids=message_id)
							await client.forward_messages(dialog.id, messages)						
					else:
						await client.send_message(dialog.id, account["promo_message"])
					print(colored(f"Promo message sent to group {dialog.id} for account {account['phone_number']}", "green"))
					count_messages += 1
				except Exception as e:
					print(colored(f"Error sending message to group {dialog.id} for account {account['phone_number']}: {str(e)}", "red"))
					count_fail_messages += 1
				time_interval = account["time_interval"] * 60
				await asyncio.sleep(time_interval)
		print("-----------------------------")
		print(colored("Total Groups: "+ str(count_groups), "green"))
		print(colored("Total Messages: "+ str(count_messages), "green"))
		print(colored("Failed Messages: "+ str(count_fail_messages), "red"))	

async def reply_to_private_messages(client, account):
    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        if hasattr(event, 'message') and isinstance(event.message, types.Message):
            if isinstance(event.message.peer_id, types.PeerUser):
                try:
                    sender = await event.get_sender()
                    await event.reply(account["reply_message"])
                    print(colored(f"Replied to private message for account {account['phone_number']} to sender: ({sender.username}) {sender.id}", "green"))
                except Exception as e:
                    print(colored(f"Error replying to private message for account {account['phone_number']}: {str(e)}", "red"))
    
    return handler

async def main():
	while True:
		tasks = []
		for account in accounts:
			api_id = account["api_id"]
			api_hash = account["api_hash"]
			phone_number = account["phone_number"]
			session_name = account["session_name"]

			client = TelegramClient(session_name, api_id, api_hash)
			try:
				await client.start(phone_number)
				print(colored(f"Connected and authorized as {phone_number}", "green"))
				client.add_event_handler(await reply_to_private_messages(client, account))

				task_send = asyncio.create_task(send_promo_messages(client, account))
				tasks.append(task_send)

			except Exception as e:
				print(colored(f"Error processing account {phone_number}: {str(e)}", "red"))

		await asyncio.gather(*tasks)

if __name__ == "__main__":
	asyncio.run(main())

colorama.deinit()
