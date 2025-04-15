from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN, ADMIN_ID, UA_CARD, CRYPTO_WALLET

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    text = (
        "Привет! Я бот-магазин виртуальной валюты.

"
        "Цена: 1$ = 1,000,000 в игре.

"
        "Чтобы купить — напиши /buy"
    )
    await msg.answer(text)

@dp.message_handler(commands=["buy"])
async def buy(msg: types.Message):
    text = (
        "Вы можете оплатить одним из способов:

"
        f"1. На украинскую карту:
<code>{UA_CARD}</code>
"
        f"2. Криптой:
<code>{CRYPTO_WALLET}</code>

"
        "После оплаты отправьте сюда:
"
        "- Фото чека
"
        "- Или последние 4 цифры карты отправителя"
    )
    await msg.answer(text, parse_mode="HTML")

@dp.message_handler(lambda msg: msg.chat.id == ADMIN_ID and msg.reply_to_message)
async def admin_confirm(msg: types.Message):
    await msg.reply_to_message.reply("✅ Оплата подтверждена. Товар отправлен.")
    await msg.answer("Готово, заказ обработан.")

@dp.message_handler()
async def receive_payment(msg: types.Message):
    await bot.send_message(ADMIN_ID,
        f"Новая заявка от @{msg.from_user.username or msg.from_user.id}:
{msg.text}")
    if msg.photo:
        await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id,
            caption=f"Чек от @{msg.from_user.username or msg.from_user.id}")
    await msg.answer("Оплата отправлена на проверку. Ожидайте подтверждения.")

if __name__ == "__main__":
    executor.start_polling(dp)
