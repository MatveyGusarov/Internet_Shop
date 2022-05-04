import logging
import sqlite3
import config
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message


class Database:
    def __init__(self, base):
        self.conn = sqlite3.connect(str(base))
        self.cur = self.conn.cursor()

    async def print_test_goods(self):
        for value in self.cur.execute("SELECT * FROM products"):
            print(value)

    async def print_test_admins(self):
        for value in self.cur.execute("SELECT * FROM administrators"):
            print(value)

    async def print_test_suples(self):
        for value in self.cur.execute("SELECT * FROM suppliers"):
            print(value)

    async def print_test_customs(self):
        for value in self.cur.execute("SELECT * FROM customers"):
            print(value)

    async def check_account(self, id):
        result = self.cur.execute(f"SELECT * FROM customers WHERE id = {id}").fetchall()
        if len(result) == 0:
            result = self.cur.execute(f"SELECT * FROM suppliers WHERE id = {id}").fetchall()
        if len(result) == 0:
            result = self.cur.execute(f"SELECT * FROM administrators WHERE id = {id}").fetchall()

        return list(result)

    async def get_mailing_list_customers(self):
        result = self.cur.execute(f"SELECT * FROM customers")

        return list(result)

    async def get_mailing_list_suples(self):
        result = self.cur.execute(f"SELECT * FROM suppliers")

        return list(result)

    async def get_is_account_active(self, id):
        result = self.cur.execute(f"SELECT type FROM customers WHERE id = {id}").fetchall()
        if len(result) == 0:
            result = self.cur.execute(f"SELECT type FROM suppliers WHERE id = {id}").fetchall()
            if len(result) == 0:
                result = self.cur.execute(f"SELECT type FROM administrators WHERE id = {id}").fetchall()

        return list(result)

    async def freeze_account(self, id):
        result = self.cur.execute(f"SELECT type FROM customers WHERE id = {id}").fetchall()
        if len(result) == 0:
            result = self.cur.execute(f"SELECT type FROM suppliers WHERE id = {id}").fetchall()
            if len(result) == 0:
                result = self.cur.execute(f"SELECT type FROM administrators WHERE id = {id}").fetchall()
                if len(result) == 0:
                    return 1
                else:
                    self.cur.execute(f"UPDATE administrators SET type = {1} WHERE id = {id}")
                    self.conn.commit()
            else:
                self.cur.execute(f"UPDATE suppliers SET type = {1} WHERE id = {id}")
                self.conn.commit()
        else:
            self.cur.execute(f"UPDATE customers SET type = {1} WHERE id = {id}")
            self.conn.commit()

        return 0

    async def unlock_account(self, id):
        result = self.cur.execute(f"SELECT type FROM customers WHERE id = {id}").fetchall()
        if len(result) == 0:
            result = self.cur.execute(f"SELECT type FROM suppliers WHERE id = {id}").fetchall()
            if len(result) == 0:
                result = self.cur.execute(f"SELECT type FROM administrators WHERE id = {id}").fetchall()
                if len(result) == 0:
                    return 1
                else:
                    self.cur.execute(f"UPDATE administrators SET type = {0} WHERE id = {int(id)}")
                    self.conn.commit()
            else:
                self.cur.execute(f"UPDATE suppliers SET type = {0} WHERE id = {int(id)}")
                self.conn.commit()
        else:
            self.cur.execute(f"UPDATE customers SET type = {0} WHERE id = {int(id)}")
            self.conn.commit()

        return 0

    async def delete_account(self, id):
        result = self.cur.execute(f"SELECT type FROM customers WHERE id = {id}").fetchall()
        if len(result) == 0:
            result = self.cur.execute(f"SELECT type FROM suppliers WHERE id = {id}").fetchall()
            if len(result) == 0:
                result = self.cur.execute(f"SELECT type FROM administrators WHERE id = {id}").fetchall()
                if len(result) == 0:
                    return 1
                else:
                    self.cur.execute(f"DELETE FROM administrators WHERE id = {int(id)}")
                    self.conn.commit()
            else:
                self.cur.execute(f"DELETE FROM suppliers WHERE id = {int(id)}")
                self.conn.commit()
        else:
            self.cur.execute(f"DELETE FROM customers WHERE id = {int(id)}")
            self.conn.commit()

        return 0

    async def change_cash(self, id, change):
        result = self.cur.execute(f"SELECT cash FROM customers WHERE id = {id}").fetchall()
        self.cur.execute(f"UPDATE customers SET cash = {int(result[0][0]) + int(change)} WHERE id = {id}")
        self.conn.commit()

        return 0

    async def get_all_categories(self):
        result = self.cur.execute("SELECT DISTINCT category FROM products")

        return list(result)

    async def get_all_goods_for_categorie(self, category):
        result = self.cur.execute(f"SELECT * FROM products")

        return list(result)

    async def change_number_of_goods(self, id_good, id_user):
        result = self.cur.execute(f"SELECT number_products FROM products WHERE id = {id_good}").fetchall()
        if (len(result) == 0) or (result[0][0] == 0):
            return 1
        else:
            price = self.cur.execute(f"SELECT price FROM products WHERE id = {id_good}").fetchall()
            cash = self.cur.execute(f"SELECT cash FROM customers WHERE id = {id_user}").fetchall()
            if int(cash[0][0]) < int(price[0][0]):
                res = [cash[0][0], price[0][0]]
                return list(res)
            else:
                result = self.cur.execute(f"SELECT cash FROM customers WHERE id = {id_user}").fetchall()
                self.cur.execute(f"UPDATE customers SET cash = {int(result[0][0]) - int(price[0][0])} WHERE id = {id_user}")
                self.conn.commit()

                result = self.cur.execute(f"SELECT number_products FROM products WHERE id = {id_good}").fetchall()
                self.cur.execute(f"UPDATE products SET number_products = {int(result[0][0]) - 1} WHERE id = {id_good}")
                self.conn.commit()

                id_supplier = self.cur.execute(f"SELECT id_supplier FROM products WHERE id = {id_good}").fetchall()
                result = self.cur.execute(f"SELECT cash FROM suppliers WHERE id = {int(id_supplier[0][0])}").fetchall()
                self.cur.execute(f"UPDATE suppliers SET cash = {int(result[0][0]) + int(price[0][0])} WHERE id = {int(id_supplier[0][0])}")
                self.conn.commit()

                self.cur.execute(f'''INSERT INTO purchase_history VALUES ('{id_user}', '{id_good}',
                '{id_supplier[0][0]}', '{price[0][0]}')''')
                self.conn.commit()

        return 0

    async def put_product_in_basket(self, username, id_good):
        try:
            category = self.cur.execute(f"SELECT category FROM products WHERE id = {id_good}").fetchall()[0][0]
            name = self.cur.execute(f"SELECT name FROM products WHERE id = {id_good}").fetchall()[0][0]
            price = self.cur.execute(f"SELECT price FROM products WHERE id = {id_good}").fetchall()[0][0]
            self.cur.execute(f'''INSERT INTO {username} VALUES ('{category}', '{name}', '{price}')''')
            self.conn.commit()
            return 0
        except():
            return 1

    async def give_user_basket(self, username):
        result = self.cur.execute(f"SELECT * FROM {username}")
        return list(result)

    async def deliver_product(self, id_good, number_of_goods):
        result = self.cur.execute(f"SELECT number_products FROM products WHERE id = {id_good}").fetchall()
        if len(result) == 0:
            return 1
        else:
            self.cur.execute(f"UPDATE products SET number_products = {int(number_of_goods) + int(result[0][0])} WHERE id = {int(id_good)}")
            self.conn.commit()
            return 0

    async def put_product(self, id_product, category, name, price, description, number_products, supplier, id_supplier):
        self.cur.execute(f'''INSERT INTO products VALUES ('{id_product}', '{category}', '{name}',
            '{price}', '{description}', '{number_products}', '{supplier}', '{id_supplier}')''')
        self.conn.commit()

    async def delete_product(self, id_product):
        result = self.cur.execute(f"SELECT number_products FROM products WHERE id = {id_product}").fetchall()
        if len(result) == 0:
            return 1
        else:
            self.cur.execute(f"DELETE FROM products WHERE id = {int(id_product)}")
            self.conn.commit()
            return 0

    async def register_new_account(self, id_account, type, name, family):
        self.cur.execute(f"SELECT type FROM administrators WHERE id = {id_account}")
        if len(self.cur.fetchall()) == 0:
            self.cur.execute(f"SELECT type FROM suppliers WHERE id = {id_account}")
            if len(self.cur.fetchall()) == 0:
                self.cur.execute(f"SELECT type FROM customers WHERE id = {id_account}")
        result = self.cur.fetchall()
        if len(result) == 0:
            if type == 'administrator':
                self.cur.execute(
                    f'''INSERT INTO administrators VALUES ('{id_account}', '{name}', '{family}', 
                    '{0}')''')
                self.conn.commit()
            elif type == 'supplier':
                self.cur.execute(f'''INSERT INTO suppliers VALUES ('{id_account}', '{name}', '{family}', 
                    '{0}', '{0}', '{id_account}')''')
                self.conn.commit()
            elif type == 'customer':
                self.cur.execute(f'''INSERT INTO customers VALUES ('{id_account}', '{name}', '{family}', 
                    '{0}', '{0}', '{id_account}')''')
                self.conn.commit()

            return 0
        else:
            return 1































































# import os
#
#
# class Database:
#     customerAccounts = 0
#     supplierAccounts = 0
#     administratorAccounts = 0
#     numberOfProducts = 0
#     path = 'nullptr'
#     def __init__(self):
#         self.path = os.getcwd()
#         self.path += '/Database/'
#         if not os.path.exists(self.path):
#             os.mkdir(self.path)
#         if not os.path.exists(self.path + 'CustomersAccounts/'):
#             os.mkdir(self.path + 'CustomersAccounts/')
#         if not os.path.exists(self.path + 'SuppliersAccounts/'):
#             os.mkdir(self.path + 'SuppliersAccounts/')
#         if not os.path.exists(self.path + 'AdministratorsAccounts/'):
#             os.mkdir(self.path + 'AdministratorsAccounts/')
#         self.customerAccounts = 0
#         self.supplierAccounts = 0
#         self.administratorAccounts = 0
#         self.numberOfProducts = 0
#
#     def FindProduct(self, nameOfProduct):
#         print('ok')
#
#     def PutProduct(self, nameOfProduct):
#         pathCur = os.getcwd() + '/Database/' + nameOfProduct + '/'
#         if not os.path.exists(pathCur):
#             os.mkdir(pathCur)
#             pathCur += nameOfProduct
#             file = open("pathCur", "w+")
#             self.numberOfProducts += 1
#
#     def CheckId(self, id):
#         files = os.listdir(self.path + 'CustomersAccounts/')
#         # print(files)
#
#     # def CheckAdministratorAccount(self, id):
#     #
#     # def FreezeAdministratorAccount(self, id):
#     #
#     # def DeleteAdministratorAccount(self, id):
#     #
#     # def CheckSupplierAccount(self, id):
#     #
#     # def FreezeSuoolierAccount(self, id):
#     #
#     # def DeleteSupplierAccount(self, id):
#     #
#     # def CheckCustomerAccount(self, id):
#     #
#     # def FreezeCustomerAccount(self, id):
#     #
#     # def DeleteCustomerAccount(self, id):
#     #
#     # def DeleteHistoryOfSalesProducts(self):
#     #
#     # def DeleteHistoryOfOffersGoods(self):
