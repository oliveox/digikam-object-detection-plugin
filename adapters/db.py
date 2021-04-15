import sqlite3
import traceback

class InternalDB():

    con = None

    @classmethod
    def execute_query(cls, query, data = None):

        try:
            con = cls.get_db_connection()
            cur = con.cursor()
            result = cur.execute(query) if data == None else cur.execute(query, data)
            return result.fetchall()
        except:
            raise
        finally:
            cls.close_db_connection()


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
        result = -1
        try:
            result = cls.execute_query(cls.insert_image_objects_query, (row_id, file_hash, ' '.join(objects)))
        except:
            traceback.print_exc()
            raise

        return result

    @classmethod
    def initialise_database(cls):
        try:
            cls.execute_query(cls.create_image_objects_table)
        except:
            traceback.print_exc()
            raise
    
    @classmethod
    def get_all_external_ids(cls):
        try:
            raw_all_external_ids = cls.execute_query(cls.get_all_external_ids_query)
            formated_external_ids = map(lambda x: x[0], raw_all_external_ids)
            return formated_external_ids
        except:
            traceback.print_exc()
            raise

    get_all_external_ids_query = """
        select DISTINCT external_id from ImageObjects
    """

    insert_image_objects_query = """
        insert into ImageObjects (external_id, hash, objects)
        values (?, ?, ?)
    """

    create_image_objects_table = """
            CREATE TABLE ImageObjects
            (id integer primary key, external_id integer, hash text, objects text)
    """



if __name__ == "__main__":
    data = (23, "someradomhash", "[car,car,person,door]")

    try:
        InternalDB.initialise_database()    
    except sqlite3.OperationalError as err:
        traceback.print_exc()

    print(InternalDB.insert_image_objects(data))