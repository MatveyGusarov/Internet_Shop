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
from create_bot import DataBase

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


@dp.message_handler(commands=['test_goods'])
async def test(message: Message, state: FSMContext):
    await DataBase.print_test_goods()
    await message.answer('ALL IS OK!')


@dp.message_handler(commands=['test_admins'])
async def test_admins(message: Message, state: FSMContext):
    await DataBase.print_test_admins()
    await message.answer('ALL IS OK!')


@dp.message_handler(commands=['test_suples'])
async def test_suples(message: Message, state: FSMContext):
    await DataBase.print_test_suples()
    await message.answer('ALL IS OK!')


@dp.message_handler(commands=['test_customs'])
async def test_customs(message: Message, state: FSMContext):
    await DataBase.print_test_customs()
    await message.answer('ALL IS OK!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
