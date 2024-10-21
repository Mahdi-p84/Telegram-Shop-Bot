import mysql.connector

def get_category_data():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor(dictionary=True)
    SQL_QUERY = 'SELECT * FROM Category;'

    cursor.execute(SQL_QUERY)

    # for r in cursor:
    #     print(r)
    result = cursor.fetchall()
    return result


if __name__ == "__main__":
    print(get_category_data())
