import logging
import sqlite3
import config
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from create_bot import dp

conn = sqlite3.connect('db.db')
cur = conn.cursor()

local_data = []

#  REGISTRATION!!!

from handlers import registration
registration.register_handlers_registration(dp)

#  CUSTOMERS  DO!!!

from handlers import customer
customer.register_handlers_customer(dp)

#  SUPPLIERS DO!!!

from handlers import supplier
supplier.register_handlers_supplier(dp)

#  ADMINISTATORS DO!!!

from handlers import administrator
administrator.register_handlers_administrator(dp)

#  FOR DEBUG!!!


@dp.message_handler(commands=['test'])
async def end_deliver(message: Message, state: FSMContext):
    for value in cur.execute("SELECT * FROM products"):
        print(value)

    await message.answer('ALL IS OK!')


@dp.message_handler(commands=['test_admins'])
async def end_deliver(message: Message, state: FSMContext):
    for value in cur.execute("SELECT * FROM administrators"):
        print(value)

    await message.answer('ALL IS OK!')


@dp.message_handler(commands=['test_suples'])
async def end_deliver(message: Message, state: FSMContext):
    for value in cur.execute("SELECT * FROM suppliers"):
        print(value)

    await message.answer('ALL IS OK!')


@dp.message_handler(commands=['test_customs'])
async def end_deliver(message: Message, state: FSMContext):
    for value in cur.execute("SELECT * FROM customers"):
        print(value)

    await message.answer('ALL IS OK!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
