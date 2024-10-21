import mysql.connector
from config import *

def insert_category_data(name):
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = 'INSERT IGNORE INTO CATEGORY (name) VALUES (%s)'
    cursor.execute(SQL_QUERY, (name,))

    conn.commit()
    cursor.close()
    conn.close()
    print(f'{name} category inserted sccessfully.')


def insert_user_data(cid, first_name, user_name, role):
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = "INSERT IGNORE INTO User (cid, first_name, user_name, role) VALUES (%s, %s, %s, %s);"
    cursor.execute(SQL_QUERY, (cid, first_name, user_name, role,))        

    conn.commit()
    cursor.close()
    conn.close()
    print('user data inserted')

def insert_sale_data(user_id):
    conn = mysql.connector.connect(user='root', host='localhost', password='mahdi870@#', database='Store')
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO Sale (user_ID) VALUES (%s)"
    cursor.execute(SQL_QUERY, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print('Sale added successfully.')


def insert_sale_row_data(product_id, quantity):
    conn = mysql.connector.connect(user='root', host='localhost', password='mahdi870@#', database='Store')
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO SALE_ROW (Product_ID, Quantity) VALUES (%s, %s)"
    cursor.execute(SQL_QUERY, (product_id, quantity,))
    
    conn.commit()
    cursor.close()
    conn.close()

    print('Sale Row added successfully.')


if __name__ == "__main__":
    insert_category_data('Digital')
    insert_category_data('Clothes')
    insert_category_data('Shoes')
    insert_category_data('Stationery')

