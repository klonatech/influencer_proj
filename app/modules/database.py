import mysql.connector

def get_mysql_connection():
    print("Connecting to mysqll..")
    try:
        return mysql.connector.connect(
            host        = '195.154.69.121',
            user        = 'backend-user',
            password    = 'N2rR<=:dhVx9d3?>!@.?',
            database    = 'klona',
            port = 29877,
        )
    #mysql.connector.connect
    except Exception as e:
        print('can not connect with database following error occured ', e)


# def delete_from_s3(file_path):
#     import boto3
#     from botocore.client import Config

#     s3 = boto3.client(
#         's3',
#         endpoint_url='https://s3.us-east-1.wasabisys.com/', # specify your Wasabi region here
#         config=Config(signature_version='s3v4')
#     )

#     s3.delete_object(Bucket='klonaimg', Key=file_path)

if __name__ == '__main__':
    query = """
        select id from users
        where name = 'Rija'
    """
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    print(type(data[0][0]))