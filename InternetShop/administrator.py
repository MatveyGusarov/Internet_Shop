import sqlite3

from aiogram import types, Dispatcher
from create_bot import dp, bot
from create_bot import DataBase
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message


class check_account(StatesGroup):
    account_id = State()
    end = State()


@dp.message_handler(commands=['check_account'])
async def begin_check_account(message: Message):
    global local_data
    local_data = []
    await check_account.account_id.set()
    await message.answer('Введите id аккаунта')


@dp.message_handler(state=check_account.account_id)
async def end_check_account(message: Message, state: FSMContext):
    await check_account.end.set()
    global local_data
    local_data += [message.text]
    result = await DataBase.check_account(local_data[0])

    if len(result) == 0:
        await message.answer("This account does not exists")
    try:
        result = result[0]
        await message.answer("Id is " + result[0])
        await message.answer("Name is " + result[1])
        await message.answer("Family is " + result[2])
        await message.answer("Type is " + result[3])
        await message.answer("Cash is " + str(result[4]))
    except():
        pass

    await state.finish()


class mailing_list_customers(StatesGroup):
    text = State()
    end = State()


@dp.message_handler(commands=['mailing_customs'])
async def begin_mailing_customs(message: Message):
    global local_data
    local_data = []
    await mailing_list_customers.text.set()
    await message.answer('Введите текст рассылки')


@dp.message_handler(state=mailing_list_customers.text)
async def end_mailing_customs(message: Message, state: FSMContext):
    await mailing_list_customers.end.set()
    global local_data
    local_data += [message.text]
    customers = await DataBase.get_mailing_list_customers()
    for element in customers:
        try:
            await bot.send_message(int(element[0]), local_data[0])
        except():
            print("User " + element[0] + " closed mailing")

    await state.finish()


class mailing_list_suples(StatesGroup):
    text = State()
    end = State()


@dp.message_handler(commands=['mailing_suples'])
async def begin_mailing_suples(message: Message):
    global local_data
    local_data = []
    await mailing_list_suples.text.set()
    await message.answer('Введите текст рассылки')


@dp.message_handler(state=mailing_list_suples.text)
async def end_mailing_suples(message: Message, state: FSMContext):
    await mailing_list_suples.end.set()
    global local_data
    local_data += [message.text]
    customers = await DataBase.get_mailing_list_suples()
    for element in customers:
        try:
            await bot.send_message(int(element[0]), local_data[0])
        except():
            print("User " + element[0] + " closed mailing")

    await state.finish()


class is_account_active(StatesGroup):
    account_id = State()
    end = State()


@dp.message_handler(commands=['is_account_active'])
async def begin_is_account_active(message: Message):
    global local_data
    local_data = []
    await is_account_active.account_id.set()
    await message.answer('Введите id аккаунта')


@dp.message_handler(state=is_account_active.account_id)
async def end_check(message: Message, state: FSMContext):
    await is_account_active.end.set()
    global local_data
    local_data += [message.text]
    result = await DataBase.get_is_account_active(local_data[0])
    if len(result) != 0:
        if int(result[0][0]) == 0:
            await message.answer('Account is active')
        else:
            await message.answer('Account is frozen')
    else:
        await message.answer('This account does not exists')

    await state.finish()


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
    result = await DataBase.freeze_account(local_data[0])

    if result == 0:
        await message.answer('One moment!')
    else:
        await message.answer('This account does not exist')

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
    result = await DataBase.unlock_account(local_data[0])

    if result == 0:
        await message.answer('One moment!')
    else:
        await message.answer('This account does not exist')

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
    result = await DataBase.delete_account(local_data[0])

    if result == 0:
        await message.answer('One moment!')
    else:
        await message.answer('This account does not exist')

    await state.finish()


def register_handlers_administrator(dp: Dispatcher):
    dp.register_message_handler(begin_freeze_account, commands=['freeze_account'])
    dp.register_message_handler(begin_unlock_account, commands=['unlock_account'])
    dp.register_message_handler(begin_delete_account, commands=['delete_account'])
    dp.register_message_handler(begin_is_account_active, commands=['is_account_active'])
    dp.register_message_handler(begin_mailing_customs, commands=['mailing_customs'])
    dp.register_message_handler(begin_mailing_suples, commands=['mailing_suples'])
    dp.register_message_handler(begin_check_account, commands=['check_account'])
