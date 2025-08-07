from telethon import TelegramClient, events
import asyncio
from keep_alive import keep_alive  # добавили

# Данные API Telegram
api_id = 22736879
api_hash = "c302972286737b8e38d11290c8690558"

# ID чата, куда бот будет пересылать сообщения
target_chat_id = 4912555353

# Ключевые фразы
keywords = [
    "куплю страховку", "где купить страховку", "где купить страховку на машину", "куплю страховку на машину",
    "куплю глово", "куплю glovo",
    "куплю вольт", "куплю wolt",
    "куплю болт-фуд", "куплю boltfood",
    "куплю болт", "куплю bolt",
    "куплю аккаунт глово", "куплю аккаунт glovo",
    "куплю аккаунт вольт", "куплю аккаунт wolt",
    "куплю аккаунт болт", "куплю аккаунт bolt",
    "куплю аккаунт болт-фуд", "куплю аккаунт boltfood"
]

# Запуск клиента
client = TelegramClient("session", api_id, api_hash)

def count_keywords(text, keyword_list):
    normalized = text.lower()
    return sum(1 for kw in keyword_list if kw in normalized)

@client.on(events.NewMessage)
async def handler(event):
    if not event.message.message or not event.is_group:
        return

    text = event.message.message.strip()
    print(f"📥 Получено сообщение: {text}")

    matches = count_keywords(text, keywords)
    print(f"✅ Совпадений: {matches}")

    if matches >= 1:
        sender = await event.get_sender()
        chat = await event.get_chat()

        sender_username = sender.username or "профиль"
        sender_link = f"https://t.me/{sender.username}" if sender.username else "нет ссылки"

        group_title = getattr(chat, 'title', 'Группа')
        group_link = f"https://t.me/c/{str(chat.id)[4:]}" if str(chat.id).startswith("-100") else "нет ссылки"

        msg = (
            f"🔎 *Найден лид:*\n"
            f"*Текст:* {text}\n"
            f"*Отправитель:* {sender_username}\n"
            f"*Ссылка:* [профиль]({sender_link})\n"
            f"*Группа:* {group_title}\n"
            f"*Ссылка на группу:* [перейти]({group_link})"
        )

        try:
            await client.send_message(target_chat_id, msg, parse_mode="markdown")
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщения: {e}")

# 🟢 Важно: Запускаем keep_alive
keep_alive()

print("✅ Сканер запущен. Ожидаем новые сообщения...")
client.start()
client.run_until_disconnected()
