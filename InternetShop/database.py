import sqlite3 as sq


def sql_start():
    global base
    global cur
    base = sq.connect('database_new.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')

    base.execute('CREATE TABLE IF NOT EXISTS menu(product_name TEXT, price TEXT, information TEXT)')
    base.commit()


async def sql_add_comand(state):
    async with state.proxy() as date:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()






















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
