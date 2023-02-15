from .connection import UseDatabase
from mysql.connector import connect, Error
from .connection import UseDatabase
prod_name = "zxc"
prod_price = 777
try:
    with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="internet"
    ) as connection:
        show_db_query = "SELECT prod_id FROM product where prod_id = 3"

        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            connection.commit()

except Error as e:
    print(e)

