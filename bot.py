import logging
from aiogram import Bot, Dispatcher, types, executor
import sqlite3
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# Подключение к базе
conn = sqlite3.connect(config.DB_PATH)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY, user TEXT, name TEXT, description TEXT)")
conn.commit()

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🍳 Добавить рецепт", "📖 Мои рецепты")
    await msg.answer("Привет, шеф 👨‍🍳!\nНажми кнопку ниже, чтобы начать.", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "🍳 Добавить рецепт")
async def add_recipe(msg: types.Message):
    await msg.answer("Введите название блюда:")
    dp.register_message_handler(save_name, state="waiting_for_name")

async def save_name(msg: types.Message):
    name = msg.text
    cur.execute("INSERT INTO recipes (user, name, description) VALUES (?, ?, ?)", (msg.from_user.id, name, "Описание не указано"))
    conn.commit()
    await msg.answer("✅ Рецепт сохранён!")

@dp.message_handler(lambda msg: msg.text == "📖 Мои рецепты")
async def my_recipes(msg: types.Message):
    cur.execute("SELECT name FROM recipes WHERE user=?", (msg.from_user.id,))
    recipes = cur.fetchall()
    if recipes:
        await msg.answer("📚 Твои рецепты:\n" + "\n".join([r[0] for r in recipes]))
    else:
        await msg.answer("Пока нет рецептов 😔")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
