import sqlite3
import traceback

class InternalDB():

    con = None

    @classmethod
    def get_db_connection(cls):
        if cls.con == None:
            cls.con = sqlite3.connect('/db/plugin.db'); 

        return cls.con

    @classmethod
    def close_db_connection(cls):
        cls.con.commit()
        cls.con.close()

        cls.con = None

    @classmethod
    def insert_image_objects(cls, row_id, file_hash, objects):
        con = cls.get_db_connection()

        cur = con.cursor()
        cur.execute('''insert into ImageObjects (external_id, hash, objects)
            values (?, ?, ?)''', (row_id, file_hash, ' '.join(objects)))

        cls.close_db_connection()

        return cur.lastrowid

    @classmethod
    def initialise_database(cls):
        con = cls.get_db_connection()
        cur = con.cursor()
        
        cur.execute("""CREATE TABLE ImageObjects
            (id integer primary key, external_id integer, hash text, objects text)""")

        cls.close_db_connection()
    
    @classmethod
    def get_all_external_ids(cls):
        con = cls.get_db_connection()
        cur = con.cursor()

        raw_all_external_ids = cur.execute(cls.get_all_external_ids_query).fetchall()
        formated_external_ids = map(lambda x: x[0], raw_all_external_ids)

        cls.close_db_connection()

        return formated_external_ids

    get_all_external_ids_query = """
        select DISTINCT external_id from ImageObjects
    """

if __name__ == "__main__":
    data = (23, "someradomhash", "[car,car,person,door]")

    try:
        InternalDB.initialise_database()    
    except sqlite3.OperationalError as err:
        traceback.print_exc()

    print(InternalDB.insert_image_objects(data))