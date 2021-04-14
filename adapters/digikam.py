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
        result = cur.execute(DigiKamAdapter.get_all_imported_entities_query).fetchall()

        # con.commit()
        # con.close()

        return result

    @classmethod
    def insert_tag(cls, parent_id, tag_name):
        con = cls.get_db_connection()
        cur = con.cursor()

        try:
            result = cur.execute(DigiKamAdapter.insert_tag_query, (parent_id, tag_name)).fetchone()[0]
        except Exception as err:
            result = cur.execute(DigiKamAdapter.get_tag_query, (parent_id, tag_name)).fetchone()[0]

        # con.commit()
        # con.close()

        return result


    @classmethod
    def insert_image_tag(cls, image_id, tag_id):
        con = cls.get_db_connection()
        cur = con.cursor()

        result = cur.execute(DigiKamAdapter.insert_image_tag_query, (image_id, tag_id))

        # con.commit()
        # con.close()

        return result


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
    result = DigiKamAdapter.get_all_imported_entities()

    for row in result:
        print(row)
            
