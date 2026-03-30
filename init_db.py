import pymysql
import pymysql.constants.CLIENT

def main():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
        )
        cursor = conexion.cursor()
        with open('setup_mysql.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        cursor.execute(sql)
        conexion.commit()
        conexion.close()
        print("Script ejecutado correctamente.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
