import sqlite3
import traceback
from sqlite3.dbapi2 import IntegrityError

from config import DIGIKAM_DB_PATH, SQLITE_MAX_VARIABLE_NUMBER

class DigiKamAdapter:

    con = None

    @classmethod
    def execute_query(cls, query, data = None, get_last_row_id = False):
        
        try:
            con = cls.get_db_connection()
            cur = con.cursor()
            result = cur.execute(query) if data == None else cur.execute(query, data)

            if get_last_row_id:
                return result.lastrowid

            return result.fetchall()
        except:
            raise
        finally:
            cls.close_db_connection()   

    @classmethod
    def get_db_connection(cls):

        try :
            if cls.con == None:
                cls.con = sqlite3.connect(DIGIKAM_DB_PATH)
            
            return cls.con
        except sqlite3.OperationalError as e:
            print("Check if the digikam database path is correct")
            raise e

    @classmethod
    def close_db_connection(cls):
        if cls.con != None:
            cls.con.commit()
            cls.con.close()

            cls.con = None

    @classmethod
    def get_all_imported_entities(cls):
        try:
            result = cls.execute_query(cls.get_all_imported_entities_query)
            return result
        except:
            traceback.print_exc()
            raise

    @classmethod
    def get_imported_entities_with_specific_ids(cls, ids):
        result = []
        counter = 0

        # query in small batches - sqlite limitation
        while True:
            start_index = counter * SQLITE_MAX_VARIABLE_NUMBER

            if (start_index >= len(ids)): break

            end_index = start_index + SQLITE_MAX_VARIABLE_NUMBER
            batch_ids = ids[start_index:end_index]

            try:
                batch_result = cls.execute_query(cls.get_imported_entities_with_specific_ids_query(len(batch_ids)), batch_ids)
            except Exception:
                traceback.print_exc()
                raise

            result.extend(batch_result)

            counter+=1

        return result

    @classmethod
    def insert_tag(cls, parent_id, tag_name):
        result = -1
        try:
            result = cls.execute_query(cls.insert_tag_query, (parent_id, tag_name), get_last_row_id = True)
        except IntegrityError:
            result = cls.execute_query(cls.get_tag_query, (parent_id, tag_name))[0][0]
        except Exception:
            traceback.print_exc()
            raise

        return result


    @classmethod
    def insert_image_tag(cls, image_id, tag_id):
        result = -1
        try:
            result = cls.execute_query(cls.insert_image_tag_query, (image_id, tag_id))
        except sqlite3.IntegrityError:
            pass
        except Exception:
            traceback.print_exc()
            raise

        return result
    
    @classmethod
    def get_all_image_ids(cls):
        try:
            raw_all_image_ids = cls.execute_query(cls.get_all_image_ids_query)
            formated_all_image_ids = list(map(lambda x: x[0], raw_all_image_ids))

            return formated_all_image_ids
        except:
            traceback.print_exc()
            raise

    # status = 1 means in Digikam that file exists, not deleted
    def get_imported_entities_with_specific_ids_query(args_length):
        
        query = """
            select i.id, a.relativePath || "/" || i.name as fullPath, i.uniqueHash from
            (
            select * from Images
            where id in ({seq}) and status = 1
            ) i
            join Albums a
            on a.id = i.album
            """.format(seq=", ".join(["?"]*args_length))
        
        return query

    get_all_image_ids_query = """
        select id from Images
    """

    get_all_imported_entities_query = """select i.id, a.relativePath || "/" || i.name as fullPath, i.uniqueHash from Images i
        join Albums a
        on a.id = i.album
        """

    insert_tag_query = '''
        insert into Tags (pid, name)
        values (?, ?)
        '''
    
    get_tag_query = """
        select id from Tags
        where pid = ? and name like ?
        """

    insert_image_tag_query = """
        insert into ImageTags (imageid, tagid)
        values (?, ?)
        """

if __name__ == "__main__":
    # result = DigiKamAdapter.get_imported_entities_with_specific_ids([13,14,15, 16, 17, 18])
    result = DigiKamAdapter.insert_tag(0, "test1234")

    for row in result:
        print(row)
            

