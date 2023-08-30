from . import database

def get_user_messages(offset, limit):
    try:
        connection = database.get_mysql_connection()
        # query = f"""
        #     SELECT *,
        #         DATE(created_at) AS created_at_date,
        #         TIME(created_at) AS created_at_time
        #     FROM user_messages
        #     ORDER BY created_at_date DESC, created_at_time ASC
        #     LIMIT {limit} OFFSET {offset}
        # """
        query = f"""
        SELECT m.message,
               DATE(m.created_at) AS created_at_date,
               TIME(m.created_at) AS created_at_time,
               u.name AS sender_name,
               m.sender_id
        FROM user_messages AS m
        JOIN users AS u ON m.sender_id = u.id
        ORDER BY created_at_date DESC, created_at_time ASC
        LIMIT {limit} OFFSET {offset}
        """
        cursor = connection.cursor()
        cursor.execute(query)

    except Exception as e:
        print("Error occured while fetching User messages\n ", e)

    else:
        # print('data fetched ', cursor.fetchall())
        return cursor.fetchall()

    finally:
        connection.close()

def approve_entire_post(post_id, value):
    connection = database.get_mysql_connection()
    try:
        query = """
        UPDATE attachments
        SET approved = %s
        WHERE post_id = %s
        """
        cursor = connection.cursor()
        cursor.execute(query, (value, post_id))
        print(query, 'values ', value, post_id)
        connection.commit()
        return 1
        
    except Exception as e:
        print('error occured while approving post ', e)
        return 0
        
    finally:
        connection.close()

def update_checkbox_value(file_name, value, column):
    print('updating checkbox')
    connection = database.get_mysql_connection()
    try:
        # cursor, connection = database.get_mysql_connection()
        query = f"""
        UPDATE attachments
        SET {column} = %s
        WHERE filename=%s
        """
        cursor = connection.cursor()
        print('query ', query)
        cursor.execute(query, (value, file_name))
        connection.commit()
        # print('updated nsfw')
        return 1
        
    except Exception as e:
        print(f'error {e} occured')
        return 0
        
    finally:
        connection.close()

def disapprove_row(file_name):
    connection = database.get_mysql_connection()
    try:
        query = f"""
            UPDATE attachments
            SET approved='-1'
            WHERE filename='{file_name[21:]}'
        """
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        return 1
        
    except Exception as e:
        print('error occured while disapproving ', e)
        print('disapproved ', file_name[21:])
        
    finally:
        connection.close()

def delete_row(file_name):
    connection = database.get_mysql_connection()
    try:
        query = f"""
        DELETE FROM attachments
        WHERE filename='{file_name[21:]}'
        """
        cursor = connection.cursor()
        print('delete query ', query)
        cursor.execute(query)
        connection.commit()
        return 1
    except Exception as e:
        print('error occured while deleting row ', e)
    finally:
        connection.close()
# def update_approve_value()