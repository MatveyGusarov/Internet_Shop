import sqlite3
import random

from aiogram import types, Dispatcher
from create_bot import dp, bot
from create_bot import DataBase
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

conn = sqlite3.connect('db.db')
cur = conn.cursor()


class deliver_product(StatesGroup):
    product_id = State()
    number_products = State()
    end = State()


@dp.message_handler(commands=['deliver_product'])
async def begin_deliver_product(message: Message):
    global local_data
    local_data = []
    await deliver_product.product_id.set()
    await message.answer('Введите id товара')


@dp.message_handler(state=deliver_product.product_id)
async def get_number(message: Message):
    await deliver_product.number_products.set()
    global local_data
    await message.answer('Введите количество поставляемых единиц товара')
    local_data += [message.text]


@dp.message_handler(state=deliver_product.number_products)
async def end_deliver(message: Message, state: FSMContext):
    await deliver_product.end.set()
    global local_data
    local_data += [message.text]
    result = await DataBase.deliver_product(local_data[0], local_data[1])
    if result == 0:
        await message.answer('One moment!')
    else:
        await message.answer('This product does not exist')

    await state.finish()


class put_product(StatesGroup):
    product_category = State()
    name = State()
    price = State()
    description = State()
    end = State()


@dp.message_handler(commands=['put_product'])
async def begin_put_product(message: Message):
    global local_data
    local_data = []
    await put_product.product_category.set()
    id_product = random.randint(1000000000, 10000000000)
    local_data += [id_product]
    await message.answer('Введите категорию товара')


@dp.message_handler(state=put_product.product_category)
async def get_name(message: Message, state: FSMContext):
    if message.text == 'end':
        await state.finish()
    else:
        await put_product.name.set()
        global local_data
        await message.answer('Введите имя товара')
        local_data += [message.text]


@dp.message_handler(state=put_product.name)
async def get_price(message: Message, state: FSMContext):
    if message.text == 'end':
        await state.finish()
    else:
        await put_product.price.set()
        await message.answer('Введите цену товара ($)')
        global local_data
        local_data += [message.text]


@dp.message_handler(state=put_product.price)
async def get_description(message: Message, state: FSMContext):
    if message.text == 'end':
        await state.finish()
    else:
        await put_product.description.set()
        await message.answer('Введите описание товара')
        global local_data
        local_data += [message.text]


@dp.message_handler(state=put_product.description)
async def end(message: Message, state: FSMContext):
    if message.text == 'end':
        await state.finish()
    else:
        global local_data
        local_data += [message.text]
        local_data += [0]
        username = message.from_user.username
        local_data += [username]
        local_data += [message.from_user.id]
        await DataBase.put_product(local_data[0], local_data[1], local_data[2], local_data[3], local_data[4],
                                   local_data[5], local_data[6], local_data[7])

        await state.finish()


class delete_product(StatesGroup):
    product_id = State()  # laptops, Phones, computers
    end = State()


@dp.message_handler(commands=['delete_product'])
async def begin_delete_product(message: Message):
    global local_data
    local_data = []
    await delete_product.product_id.set()
    await message.answer('Введите id товара')


@dp.message_handler(state=delete_product.product_id)
async def end_delete(message: Message, state: FSMContext):
    await delete_product.end.set()
    global local_data
    local_data += [message.text]
    result = await DataBase.delete_product(local_data[0])
    if result == 0:
        await message.answer('One moment!')
    else:
        await message.answer('This product does not exist')

    await state.finish()


def register_handlers_supplier(dp: Dispatcher):
    dp.register_message_handler(begin_deliver_product, commands=['deliver_product'])
    dp.register_message_handler(begin_put_product, commands=['put_product'])
    dp.register_message_handler(begin_delete_product, commands=['delete_product'])
