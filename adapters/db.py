import sqlite3

class InternalDB():

    @classmethod
    def get_db_connection(cls):
        return sqlite3.connect('/db/plugin.db'); 

    @classmethod
    def insert_image_objects(cls, row_id, file_hash, objects):
        con = cls.get_db_connection()

        cur = con.cursor()
        cur.execute('''insert into ImageObjects (external_id, hash, objects)
            values (?, ?, ?)''', (row_id, file_hash, ' '.join(objects)))

        con.commit()
        con.close()

        return cur.lastrowid

    @classmethod
    def initialise_database(cls):
        con = cls.get_db_connection()
        cur = con.cursor()
        
        cur.execute("""CREATE TABLE ImageObjects
            (id integer primary key, external_id integer, hash text, objects text)""")

        con.commit()
        con.close()
    
    @classmethod
    def get_all_external_ids(cls):
        con = cls.get_db_connection()
        cur = con.cursor()

        raw_all_external_ids = cur.execute(cls.get_all_external_ids_query).fetchall()
        formated_external_ids = map(lambda x: x[0], raw_all_external_ids)

        con.commit()
        con.close()

        return formated_external_ids

    get_all_external_ids_query = """
        select DISTINCT external_id from ImageObjects
    """

if __name__ == "__main__":
    data = (23, "someradomhash", "[car,car,person,door]")

    try:
        InternalDB.initialise_database()    
    except sqlite3.OperationalError as err:
        print("Error: {}".format(err))

    print(InternalDB.insert_image_objects(data))