import sqlite3

from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

conn = sqlite3.connect('db.db')
cur = conn.cursor()


class put_money(StatesGroup):
    begin = State()
    count = State()


@dp.message_handler(commands=['put_money'])
async def begin_put_money(message: Message, state: FSMContext):
    global local_data
    local_data = []
    await put_money.begin.set()
    await message.answer('Введите количество денег')


@dp.message_handler(state=put_money.begin)
async def get_count_of_money(message: Message, state: FSMContext):
    await put_money.count.set()
    global local_data
    local_data += [message.text]
    cur.execute(f"SELECT cash FROM customers WHERE id = {message.from_user.id}")
    result = cur.fetchall()
    cur.execute(f"UPDATE customers SET cash = {int(result[0][0]) + int(local_data[0])} WHERE id = {message.from_user.id}")
    conn.commit()
    await state.finish()


class find_product(StatesGroup):
    begin = State()
    category = State()


@dp.message_handler(commands=['find_product'])
async def begin_find_product(message: Message, state: FSMContext):
    global local_data
    local_data = []
    await find_product.begin.set()
    await message.answer('Введите категорию товара')
    for value in cur.execute("SELECT DISTINCT category FROM products"):
        await message.answer(value[0])


@dp.message_handler(state=find_product.begin)
async def get_category(message: Message, state: FSMContext):
    await find_product.category.set()
    global local_data
    local_data += [message.text]
    for value in cur.execute(f"SELECT * FROM products"):
        if value[1] == local_data[0]:
            await message.answer(value[2] + ' ' + value[3])
    await state.finish()


class buy_product(StatesGroup):
    begin = State()
    id = State()


@dp.message_handler(commands=['buy_product'])
async def begin_buy_product(message: Message, state: FSMContext):
    global local_data
    local_data = []
    await buy_product.begin.set()
    await message.answer('Введите id товара, который собираетесь купить')


@dp.message_handler(state=buy_product.begin)
async def get_category(message: Message, state: FSMContext):
    await buy_product.id.set()
    global local_data
    local_data += [message.text]
    cur.execute(f"SELECT number_products FROM products WHERE id = {local_data[0]}")
    result = cur.fetchall()
    if (len(result) == 0) or (result[0][0] == 0):
        await message.answer('Этого товара нет в наличии')
    else:
        cur.execute(f"SELECT price FROM products WHERE id = {local_data[0]}")
        price = cur.fetchall()
        cur.execute(f"SELECT cash FROM customers WHERE id = {message.from_user.id}")
        cash = cur.fetchall()
        if int(cash[0][0]) < int(price[0][0]):
            await message.answer("У Вас недостаточно средств")
        else:
            cur.execute(f"SELECT cash FROM customers WHERE id = {message.from_user.id}")
            result = cur.fetchall()
            cur.execute(f"UPDATE customers SET cash = {int(result[0][0]) - int(price[0][0])} WHERE id = {message.from_user.id}")
            conn.commit()

            cur.execute(f"SELECT number_products FROM products WHERE id = {local_data[0]}")
            result = cur.fetchall()
            cur.execute(f"UPDATE products SET number_products = {int(result[0][0]) - 1} WHERE id = {local_data[0]}")
            conn.commit()

            cur.execute(f"SELECT id_supplier FROM products WHERE id = {local_data[0]}")
            id_supplier = cur.fetchall()
            cur.execute(f"SELECT cash FROM suppliers WHERE id = {int(id_supplier[0][0])}")
            result = cur.fetchall()
            cur.execute(f"UPDATE suppliers SET cash = {int(result[0][0]) + int(price[0][0])} WHERE id = {int(id_supplier[0][0])}")
            conn.commit()

    await state.finish()


def register_handlers_customer(dp: Dispatcher):
    dp.register_message_handler(begin_put_money, commands=['put_money'])
    dp.register_message_handler(begin_find_product, commands=['find_product'])
    dp.register_message_handler(begin_buy_product, commands=['buy_product'])
