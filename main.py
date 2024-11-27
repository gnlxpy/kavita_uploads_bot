import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import os

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

UPLOAD_DIR = "./uploads"  # Папка для сохранения файлов
MAX_FILE_SIZE = 50 * 1024 * 1024  # Максимальный размер файла - 50 МБ

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Логирование
logging.basicConfig(level=logging.INFO)

# Проверка и создание папки для загрузок
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Привет! Отправь мне файлы .epub размером до 50 МБ.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.reply("Просто отправь мне файлы .epub, и я сохраню их на сервере.")


@dp.message(F.document)
async def handle_document(message: types.Message):
    document = message.document

    if not document.file_name.endswith(".epub"):
        await message.reply("Пожалуйста, отправьте файл в формате .epub.")
        return

    if document.file_size > MAX_FILE_SIZE:
        await message.reply("Файл слишком большой. Максимальный размер — 50 МБ.")
        return

    file_path = os.path.join(UPLOAD_DIR, document.file_name)

    # Загрузка файла с использованием bot.download()
    file = await bot.download(document.file_id, destination=file_path)
    await message.reply(f"Файл {document.file_name} успешно сохранен.")


async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
