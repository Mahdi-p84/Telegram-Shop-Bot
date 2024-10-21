import mysql.connector

def create_database():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#')
    cursor = conn.cursor()
    SQL_QUERY = 'DROP DATABASE IF EXISTS Store'
    cursor.execute(SQL_QUERY)

    SQL_QUERY = 'CREATE DATABASE Store'
    cursor.execute(SQL_QUERY)

    conn.commit()
    cursor.close()
    conn.close()

    print('Database Store created.')



def create_user_table():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = """
        CREATE TABLE IF NOT EXISTS `User`(
                    `CID`             BIGINT UNSIGNED NOT NULL PRIMARY KEY, 
                    `first_name`      VARCHAR(100) NOT NULL, 
                    `last_name`       VARCHAR(150),
                    `user_name`       VARCHAR(100),
                    `is blocked`      ENUM('Yes' , 'No') DEFAULT 'No',
                    `role`            ENUM('Admin', 'Customer') DEFAULT 'Customer',
                    `address`         VARCHAR(500),
                    `phone`           VARCHAR(18),
                    `register_date`   DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `last-update`     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
"""

    cursor.execute(SQL_QUERY)
    conn.commit()
    cursor.close()
    conn.close()

    print('User Table created.')


def create_product_table():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = """
        CREATE TABLE IF NOT EXISTS Product( 
                    `ID`              MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `name`            VARCHAR(100) NOT NULL,
                    `desciption`      TEXT,
                    `category_id`     INT UNSIGNED,
                    `price`           DOUBLE(10,2) NOT NULL,
                    `inventory`       SMALLINT UNSIGNED NOT NULL DEFAULT 0,
                    `register_date`   DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `last-update`     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES Category(ID));
"""

    cursor.execute(SQL_QUERY)
    conn.commit()
    cursor.close()
    conn.close()

    print('Product Table created.')


def create_sale_table():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = """
        CREATE TABLE IF NOT EXISTS Sale (
                    `ID`              MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `date`            DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `user_ID`         BIGINT UNSIGNED NOT NULL,
                    `last-update`     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_ID) REFERENCES User(CID));
"""

    cursor.execute(SQL_QUERY)
    conn.commit()
    cursor.close()
    conn.close()

    print('Sale Table created.')


def create_sale_row_table():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = """
        CREATE TABLE IF NOT EXISTS SALE_ROW (
                    `Invoice_ID`      MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    `Product_ID`      MEDIUMINT UNSIGNED NOT NULL,
                    `Quantity`        TINYINT UNSIGNED NOT NULL,
                    `last-update`     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (Invoice_ID) REFERENCES Sale(ID),
                    FOREIGN KEY (Product_ID) REFERENCES Product(ID),
                    PRIMARY KEY (Invoice_ID , Product_ID));
"""

    cursor.execute(SQL_QUERY)
    conn.commit()
    cursor.close()
    conn.close()

    print('Sale_Row Table created.')


def create_category_table():
    conn = mysql.connector.connect(user = 'root', host = 'localhost', password = 'mahdi870@#', database = 'Store')
    cursor = conn.cursor()
    SQL_QUERY = """
        CREATE TABLE IF NOT EXISTS Category(
                    `ID`               INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `name`             VARCHAR(100) NOT NULL UNIQUE,
                    `register_date`    DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `last-update`      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
"""

    cursor.execute(SQL_QUERY)
    conn.commit()
    cursor.close()
    conn.close()

    print('Category Table created.')


if __name__ == "__main__":
    create_database()
    create_user_table()
    create_category_table()
    create_product_table()
    create_sale_table()
    create_sale_row_table()
