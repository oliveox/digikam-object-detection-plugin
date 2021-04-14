import sqlite3

class DigiKamAdapter:

    con = None

    @classmethod
    def get_db_connection(cls):
        if cls.con == None:
            cls.con = sqlite3.connect('/digikam/db/digikam4.db')
        
        return cls.con

    @classmethod
    def close_db_connection(cls):
        if cls.con != None:
            cls.con.commit()
            cls.con.close()

            cls.con = None

    @classmethod
    def get_all_imported_entities(cls):
        con = cls.get_db_connection()
        cur = con.cursor()
        result = cur.execute(cls.get_all_imported_entities_query).fetchall()

        cls.close_db_connection()

        return result

    @classmethod
    def get_imported_entities_with_specific_ids(cls, ids):
        con = cls.get_db_connection()
        cur = con.cursor()

        result = cur.execute(cls.get_imported_entities_with_specific_ids_query(len(ids)), ids).fetchall()

        cls.close_db_connection()

        return result

    @classmethod
    def insert_tag(cls, parent_id, tag_name):
        con = cls.get_db_connection()
        cur = con.cursor()

        try:
            result = cur.execute(cls.insert_tag_query, (parent_id, tag_name)).fetchone()[0]
        except Exception as err:
            result = cur.execute(cls.get_tag_query, (parent_id, tag_name)).fetchone()[0]

        cls.close_db_connection()

        return result


    @classmethod
    def insert_image_tag(cls, image_id, tag_id):
        con = cls.get_db_connection()
        cur = con.cursor()

        result = cur.execute(cls.insert_image_tag_query, (image_id, tag_id))

        cls.close_db_connection()

        return result
    
    @classmethod
    def get_all_image_ids(cls):
        con = cls.get_db_connection()
        cur = con.cursor()

        # TODO - execute all queries in separated method isolated with try / catch for any execute
        raw_all_image_ids = cur.execute(cls.get_all_image_ids_query).fetchall()
        formated_all_image_ids = map(lambda x: x[0], raw_all_image_ids)

        cls.close_db_connection()

        return formated_all_image_ids

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
    result = DigiKamAdapter.get_imported_entities_with_specific_ids([13,14,15, 16, 17, 18])

    for row in result:
        print(row)
            
