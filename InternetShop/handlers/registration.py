import sqlite3

from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

conn = sqlite3.connect('db.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS products(
   id TEXT,
   category TEXT,
   name TEXT,
   price TEXT,
   description TEXT,
   number_products BIGINT,
   supplier TEXT,
   id_supplier TEXT);
""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS customers(
   id TEXT,
   name TEXT,
   family TEXT,
   type TEXT,
   cash BIGINT,
   basket TEXT);
""")
# type - freeze account or no  :  0 = not freeze and 1 = freeze
# basket - корзина продуктов, которые сопоставлены пользователю, покупатель - товары,
# которые он хочет купить, поставщие - товары, которые  он хочет поставить
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS suppliers(
   id TEXT,
   name TEXT,
   family TEXT,
   type TEXT,
   cash BIGINT,
   basket TEXT);
""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS administrators(
   id TEXT,
   name TEXT,
   family TEXT,
   type TEXT);
""")
conn.commit()


class registration(StatesGroup):
    begin = State()
    type_of_user = State()
    name = State()
    end = State()


@dp.message_handler(commands=['start'])
async def begin_registration(message: Message):
    global local_data
    local_data = []
    await registration.begin.set()
    id_account = message.from_user.id
    local_data += [id_account]
    await message.answer('Введите категорию аккаунта: administrator, supplier or customer')


@dp.message_handler(state=registration.begin)
async def get_type(message: Message):
    global local_data
    await registration.type_of_user.set()
    if message.text == 'administrator':
        local_data += ['administrator']
    elif message.text == 'supplier':
        local_data += ['supplier']
        username = message.from_user.username
        cur.execute(f"CREATE TABLE IF NOT EXISTS {username}( id TEXT);")
        conn.commit()
    elif message.text == 'customer':
        local_data += ['customer']
        username = message.from_user.username
        cur.execute(f"CREATE TABLE IF NOT EXISTS {username}( id TEXT);")
        conn.commit()
    else:
        await message.answer('Такого типа аккаунта не существует')

    await message.answer('Введите ваше имя')


@dp.message_handler(state=registration.type_of_user)
async def get_name(message: Message):
    await registration.name.set()
    global local_data
    local_data += [message.text]
    await message.answer('Введите вашу фамилию')


@dp.message_handler(state=registration.name)
async def end_registration(message: Message, state: FSMContext):
    await registration.end.set()
    global local_data
    local_data += [message.text]
    cur.execute(f"SELECT type FROM administrators WHERE id = {local_data[0]}")
    if len(cur.fetchall()) == 0:
        cur.execute(f"SELECT type FROM suppliers WHERE id = {local_data[0]}")
        if len(cur.fetchall()) == 0:
            cur.execute(f"SELECT type FROM customers WHERE id = {local_data[0]}")
    result = cur.fetchall()
    if len(result) == 0:
        if local_data[1] == 'administrator':
            cur.execute(f'''INSERT INTO administrators VALUES ('{local_data[0]}', '{local_data[2]}', '{local_data[3]}', 
            '{0}')''')
            conn.commit()
        elif local_data[1] == 'supplier':
            cur.execute(f'''INSERT INTO suppliers VALUES ('{local_data[0]}', '{local_data[2]}', '{local_data[3]}', 
            '{0}', '{0}', '{local_data[0]}')''')
            conn.commit()
        elif local_data[1] == 'customer':
            cur.execute(f'''INSERT INTO customers VALUES ('{local_data[0]}', '{local_data[2]}', '{local_data[3]}', 
            '{0}', '{0}', '{local_data[0]}')''')
            conn.commit()
    else:
        await message.answer("Аккаунт уже существует")

    await message.answer("OK")
    await state.finish()


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(begin_registration, commands=['start'])
