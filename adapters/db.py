import sqlite3

class InternalDB():

    @classmethod
    def insert_image_objects(cls, image_object_data):
        con = sqlite3.connect('/db/plugin.db')

        cur = con.cursor()
        cur.execute('''insert into ImageObjects (external_id, hash, objects)
            values (?, ?, ?)''', image_object_data)

        con.commit()
        con.close()

        return cur.lastrowid

    @classmethod
    def initialise_database(cls):
        con = sqlite3.connect('/db/plugin.db')

        cur = con.cursor()
        cur.execute("""CREATE TABLE ImageObjects
            (id integer primary key, external_id integer, hash text, objects text)""")

        con.commit()
        con.close()

if __name__ == "__main__":
    data = (23, "someradomhash", "[car,car,person,door]")

    try:
        InternalDB.initialise_database()    
    except sqlite3.OperationalError as err:
        print("Error: {}".format(err))

    print(InternalDB.insert_image_objects(data))