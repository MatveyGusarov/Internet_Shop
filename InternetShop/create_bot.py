import logging
import sqlite3
import config
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from database import Database

DataBase = Database('db.db')
conn = sqlite3.connect('db.db')
cur = conn.cursor()

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

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

cur.execute("""CREATE TABLE IF NOT EXISTS purchase_history(
    id_customs TEXT,
    id_goods TEXT,
    id_supplier TEXT,
    price TEXT);
""")
conn.commit()
