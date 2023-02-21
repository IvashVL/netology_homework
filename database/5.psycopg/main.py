# import psycopg2
import psycopg


def create_tables(connection):
    with connection.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS client(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT,
                    email TEXT
                    );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS phone(
                    phone text NOT NULL,
                    client_id INTEGER NOT NULL REFERENCES client(id),
                    PRIMARY KEY (phone, client_id)
                    );""")

        # Составной первичный ключ использован для того, чтобы разным клиентам можно было присвоить
        # одинаковые номера телефонов. Если такого требования нет, тогда первичным ключом можно сделать номер телефона

        connection.commit()


def delete_tables(connection):
    with connection.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS phone;")
        cur.execute("DROP TABLE IF EXISTS client;")
        connection.commit()


def add_client(connection, client_id, name, surname, email, phones=None):
    with connection.cursor() as cur:
        cur.execute("INSERT INTO client(id, name, surname, email) "
                    f"VALUES({client_id}, '{name}', '{surname}', '{email}');")
        if phones:
            phones_str = ', '.join((f"('{phone}', {client_id})" for phone in phones))
            query = f"INSERT INTO phone(phone, client_id) VALUES" + phones_str + ';'
            cur.execute(query)
        connection.commit()


def delete_client(connection, client_id):
    with connection.cursor() as cur:
        cur.execute(f"DELETE FROM phone WHERE client_id = {client_id};")
        cur.execute(f"DELETE FROM client WHERE id = {client_id};")
        connection.commit()


def change_client(connection, client_id, name=None, surname=None, email=None, phones=None):
    options_dict = {'name': name, 'surname': surname, 'email': email}
    options_str = ', '.join((f"{k} = '{v}'" for k, v in options_dict.items() if v))
    with connection.cursor() as cur:
        if options_str:
            query = f"UPDATE client SET " + options_str + f" WHERE id = {client_id};"
            cur.execute(query)
        if phones:
            phones_str = ', '.join((f"('{phone}', {client_id})" for phone in phones))
            query = f"DELETE FROM phone WHERE client_id = {client_id};\n" \
                    f"INSERT INTO phone(phone, client_id) VALUES" + phones_str + ';'
            cur.execute(query)
        connection.commit()


def add_phone(connection, client_id, phone):
    with connection.cursor() as cur:
        cur.execute(f"INSERT INTO phone(phone, client_id) VALUES('{phone}', {client_id});")
        connection.commit()


def delete_phone(connection, client_id, phone):
    with connection.cursor() as cur:
        cur.execute(f"DELETE FROM phone WHERE client_id = '{client_id}' AND phone = '{phone}';")
        connection.commit()


def find_client(connection, name=None, surname=None, email=None, phone=None):
    options_dict = {'name': name, 'surname': surname, 'email': email, 'phone': phone}
    options_str = ' AND '.join((f"{k} = '{v}'" for k, v in options_dict.items() if v))
    query = f"SELECT name, surname, email, phone FROM client " \
            f"LEFT JOIN phone ON client_id = id " \
            f"WHERE " + options_str + ';'
    with connection.cursor() as cur:
        cur.execute(query)
        clients = cur.fetchall()
        connection.commit()
    return clients


if __name__ == '__main__':
    with psycopg.connect(dbname='test', user="postgres", password="postgres") as conn:
    # with psycopg2.connect(database="test", user="postgres", password="postgres") as conn:
        delete_tables(conn)
        create_tables(conn)
        add_client(conn, 1, 'name1', 'surname1', '@mail1')
        add_client(conn, 2, 'name2', 'surname2', '@mail2')
        add_client(conn, 3, 'name3', 'surname3', '@mail3')
        add_client(conn, 4, 'name4', 'surname4', '@mail4', ('123', '456', '789'))
        add_client(conn, 5, 'name1', 'surname1', '@mail5')
        add_client(conn, 6, 'name6', 'surname6', '@mail6')

        delete_client(conn, 3)

        print(find_client(conn, name='name4'))

        change_client(conn, 5, phones=('12345', '09876'))
        print(find_client(conn, name='name1', surname='surname1'))
        change_client(conn, 5, name='name5', surname='surname5')
        print(find_client(conn, name='name1', surname='surname1'))

        add_phone(conn, 2, '222-222')
        add_phone(conn, 2, '333-333')
        add_phone(conn, 6, '333-333')
        print(find_client(conn, phone='333-333'))
        print(find_client(conn, name='name2'))
        delete_phone(conn, 2, '333-333')
        print(find_client(conn, name='name2'))
        print(find_client(conn, phone='333-333'))

    conn.close()
