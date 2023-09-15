import pymysql


class MYSQL_CONNECT(object):

    def __init__(self):
        self.username = ''
        self.password = ''
        self.host = ''
        self.port = 3306
        self.db_name = ''
        self.db = pymysql.connect(user=self.username, password=self.password, host=self.host, port=self.port,
                                  db=self.db_name, charset='utf8')
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def create_table(self, create_table_sql):
        db = pymysql.connect(user=self.username, password=self.password, host=self.host, port=self.port,
                             db=self.db_name, charset='utf8')
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(create_table_sql)
        db.commit()
        db.close()

    def sql_execute(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def sql_find_execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close_connect(self):
        self.db.close()


def sql_execute(sql):
    sql_cursor = MYSQL_CONNECT()
    result = sql_cursor.sql_find_execute(sql)
    sql_cursor.close_connect()
    return result
