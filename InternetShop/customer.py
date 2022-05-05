import sqlite3

from aiogram import types, Dispatcher
from create_bot import dp, bot
from create_bot import DataBase
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message


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
    result = await DataBase.change_cash(message.from_user.id, local_data[0])

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
    result = await DataBase.get_all_categories()
    for value in result:
        await message.answer(value[0])


@dp.message_handler(state=find_product.begin)
async def get_category(message: Message, state: FSMContext):
    await find_product.category.set()
    global local_data
    local_data += [message.text]
    result = await DataBase.get_all_goods_for_categorie(local_data[0])
    for value in result:
        if value[1] == local_data[0]:
            await message.answer(value[2] + ' ' + value[3] + ' id is ' + value[0])

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

    result = await DataBase.change_number_of_goods(local_data[0], message.from_user.id)
    if result == 0:
        await message.answer("Congratulations, come again!")
    else:
        if result == 1:
            await message.answer('Этого товара нет в наличии')
        else:
            await message.answer("У Вас недостаточно средств")
            await message.answer("You have " + str(result[0]))
            await message.answer("Goods costs " + str(result[1]))

    await state.finish()


class put_product_in_basket(StatesGroup):
    begin = State()
    id_product = State()


@dp.message_handler(commands=['put_in_basket'])
async def begin_put_product_in_basket(message: Message, state: FSMContext):
    global local_data
    local_data = []
    await put_product_in_basket.begin.set()
    await message.answer('Введите id товара, который собираетесь положить в корзину')


@dp.message_handler(state=put_product_in_basket.begin)
async def get_id_product(message: Message, state: FSMContext):
    await put_product_in_basket.id_product.set()
    global local_data
    local_data += [message.text]
    username = message.from_user.username
    result = await DataBase.put_product_in_basket(username, local_data[0])
    if result == 0:
        await message.answer("All is OK")
    else:
        await message.answer("Something is wrong")

    await state.finish()


class show_my_basket(StatesGroup):
    begin = State()


@dp.message_handler(commands=['show_basket'])
async def begin_show_my_basket(message: Message, state: FSMContext):
    username = message.from_user.username
    result = await DataBase.give_user_basket(username)
    for value in result:
        await message.answer(str(value[0]) + ' ' + str(value[1]) + ' ' + str(value[2]))

    await state.finish()


def register_handlers_customer(dp: Dispatcher):
    dp.register_message_handler(begin_put_money, commands=['put_money'])
    dp.register_message_handler(begin_find_product, commands=['find_product'])
    dp.register_message_handler(begin_buy_product, commands=['buy_product'])
    dp.register_message_handler(begin_put_product_in_basket, commands=['put_in_basket'])
    dp.register_message_handler(begin_show_my_basket, commands=['show_basket'])
