class Message:
    __id = None
    # czy from_id, to_id powinno być prywatne?
    from_id = None
    to_id = None
    text = None
    __creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = 0
        self.to_id = 0
        self.text = ''
        self.__creation_date = 0

    @staticmethod
    def load_message_by_id(cursor, message_id):
        sql = "SELECT id, from_id, to_id, creation_date, text FROM message WHERE id=%s"
        cursor.execute(sql, (message_id,))  # (message_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.__creation_date = data[3]
            loaded_message.text = data[4]
            return loaded_message
        else:
            return None
    
    @staticmethod
    def load_all_messages_for_user(cursor, user_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM message where to_id=%s"
        result = []
        cursor.execute(sql, (user_id,))
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            result.append(loaded_message)
        return result
    
    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, creation_date, text FROM message"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.__creation_date = row[3]
            loaded_message.text = row[4]
            ret.append(loaded_message)
        return ret

    def save_to_db(self):
        pass

    @property
    def get_id(self):
        return self.__id

    def delete(self, cursor):
        sql = "DELETE FROM message WHERE id=%s"
        cursor.execute(sql, (self.__id,))
        self.__id = -1
        cursor.close()
        return True

