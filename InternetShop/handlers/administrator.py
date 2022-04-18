import sqlite3

from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

conn = sqlite3.connect('db.db')
cur = conn.cursor()


class freeze_account(StatesGroup):
    account_id = State()  # laptops, Phones, computers
    end = State()


@dp.message_handler(commands=['freeze_account'])
async def begin_freeze_account(message: Message):
    global local_data
    local_data = []
    await freeze_account.account_id.set()
    await message.answer('Введите id аккаунта')


@dp.message_handler(state=freeze_account.account_id)
async def end_freeze(message: Message, state: FSMContext):
    await freeze_account.end.set()
    global local_data
    local_data += [message.text]
    cur.execute(f"SELECT type FROM customers WHERE id = {local_data[0]}")
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute(f"SELECT type FROM suppliers WHERE id = {local_data[0]}")
        result = cur.fetchall()
        if len(result) == 0:
            cur.execute(f"SELECT type FROM administrators WHERE id = {local_data[0]}")
            result = cur.fetchall()
            if len(result) == 0:
                await message.answer('This account does not exist')
            else:
                await message.answer('One moment!')
                cur.execute(f"UPDATE administrators SET type = {1} WHERE id = {int(local_data[0])}")
                conn.commit()
        else:
            await message.answer('One moment!')
            cur.execute(f"UPDATE suppliers SET type = {1} WHERE id = {int(local_data[0])}")
            conn.commit()
    else:
        await message.answer('One moment!')
        cur.execute(f"UPDATE customers SET type = {1} WHERE id = {int(local_data[0])}")
        conn.commit()

    await state.finish()


class unlock_account(StatesGroup):
    account_id = State()  # laptops, Phones, computers
    end = State()


@dp.message_handler(commands=['unlock_account'])
async def begin_unlock_account(message: Message):
    global local_data
    local_data = []
    await unlock_account.account_id.set()
    await message.answer('Введите id аккаунта')


@dp.message_handler(state=unlock_account.account_id)
async def end_unlock(message: Message, state: FSMContext):
    await unlock_account.end.set()
    global local_data
    local_data += [message.text]
    cur.execute(f"SELECT type FROM customers WHERE id = {local_data[0]}")
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute(f"SELECT type FROM suppliers WHERE id = {local_data[0]}")
        result = cur.fetchall()
        if len(result) == 0:
            cur.execute(f"SELECT type FROM administrators WHERE id = {local_data[0]}")
            result = cur.fetchall()
            if len(result) == 0:
                await message.answer('This account does not exist')
            else:
                await message.answer('One moment!')
                cur.execute(f"UPDATE administrators SET type = {0} WHERE id = {int(local_data[0])}")
                conn.commit()
        else:
            await message.answer('One moment!')
            cur.execute(f"UPDATE suppliers SET type = {0} WHERE id = {int(local_data[0])}")
            conn.commit()
    else:
        await message.answer('One moment!')
        cur.execute(f"UPDATE customers SET type = {0} WHERE id = {int(local_data[0])}")
        conn.commit()

    await state.finish()


class delete_account(StatesGroup):
    account_id = State()  # laptops, Phones, computers
    end = State()


@dp.message_handler(commands=['delete_account'])
async def begin_delete_account(message: Message):
    global local_data
    local_data = []
    await delete_account.account_id.set()
    await message.answer('Введите id аккаунта')


@dp.message_handler(state=delete_account.account_id)
async def end_freeze(message: Message, state: FSMContext):
    await delete_account.end.set()
    global local_data
    local_data += [message.text]
    cur.execute(f"SELECT type FROM customers WHERE id = {local_data[0]}")
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute(f"SELECT type FROM suppliers WHERE id = {local_data[0]}")
        result = cur.fetchall()
        if len(result) == 0:
            cur.execute(f"SELECT type FROM administrators WHERE id = {local_data[0]}")
            result = cur.fetchall()
            if len(result) == 0:
                await message.answer('This account does not exist')
            else:
                await message.answer('One moment!')
                cur.execute(f"DELETE FROM administrators WHERE id = {int(local_data[0])}")
                conn.commit()
        else:
            await message.answer('One moment!')
            cur.execute(f"DELETE FROM suppliers WHERE id = {int(local_data[0])}")
            conn.commit()
    else:
        await message.answer('One moment!')
        cur.execute(f"DELETE FROM customers WHERE id = {int(local_data[0])}")
        conn.commit()

    await state.finish()


def register_handlers_administrator(dp: Dispatcher):
    dp.register_message_handler(begin_freeze_account, commands=['freeze_account'])
    dp.register_message_handler(begin_unlock_account, commands=['unlock_account'])
    dp.register_message_handler(begin_delete_account, commands=['delete_account'])
