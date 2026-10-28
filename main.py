import asyncio
import os, datetime
from telethon import TelegramClient
from config import api_id, api_hash, phone_number

client = TelegramClient(f'{phone_number}.session', api_id, api_hash,
                        device_model='Desktop',
                        system_version='Windows 10',
                        app_version='4.16.0',
                        lang_code='ru',
                        system_lang_code='ru-RU')


async def list_and_choose_chat():
    """
    Print the list of your chats with number to quik choosing of the chat.
    """
    await client.start()

    dialogs = await client.get_dialogs()

    print("List of your chats:")
    for i, dialog in enumerate(dialogs):
        chat_name = dialog.name
        if dialog.is_group:
            chat_type = " (group)"
        elif dialog.is_channel:
            chat_type = " (channel)"
        else:
            chat_type = " (private)"
        print(f"{i + 1}. {chat_name}{chat_type}")

    while True:
        try:
            choice = int(input("Enter a number of chat to choose: "))
            if 1 <= choice <= len(dialogs):
                chosen_dialog = dialogs[choice - 1]
                global chat_id  # Объявляем chat_id глобальной переменной
                chat_id = chosen_dialog.entity.id
                print(f"Chosen chat: {chosen_dialog.name}")
                break
            else:
                print("Incorrect chat number. Try again.")
        except ValueError:
            print("Incorrect format. Enter a number.")

    await client.disconnect()

async def scrape_and_save_messages():
    """
    Export messages from the chat to the file.
    """
    await client.start()

    entity = await client.get_entity(chat_id)

    file_name = ""

    if hasattr(entity, 'first_name'):
        name = entity.first_name
        file_name = f"{name}_{datetime.date}.txt"
    elif hasattr(entity, 'title'):  # for groups and channels
        title = entity.title
        file_name = f"{title}_{datetime.date}.txt"
    else:  # if there is neither first_name, nor title
        file_name = f"chat_{datetime.date}.txt"

    # change symbols for file naming
    file_name = "".join(c if c.isalnum() or c == "_" else "_" for c in file_name)

    file_path = os.path.join("chat_logs", file_name)

    os.makedirs("chat_logs", exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        messages = await client.get_messages(entity, limit=10000)
        for message in messages:
            sender_name = "Unknown sender"
            if message.sender:
                if hasattr(message.sender, 'first_name'):
                    sender_name = message.sender.first_name or message.sender.last_name or "User"
                if hasattr(message.sender, 'title'):
                    sender_name = message.sender.title or "Channel"
            f.write(f'{sender_name}: {message.text}, {message.date}\n')

    print(f"Message history downloaded to the file: {file_path}")

    await client.disconnect()

async def main():
    await list_and_choose_chat()
    await scrape_and_save_messages()

if __name__ == "__main__":
    asyncio.run(main())