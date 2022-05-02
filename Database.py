# -*- coding: utf-8 -*-
import pymysql
import Constant

# 数据持久层
# owner字段为了区分fav拥有者
class Database():
    def __init__(self):
        self.password = Constant.PASSWORD
        self.db = Constant.DB
        self.host = Constant.HOST
        self.database = pymysql.connect(host=self.host, user="root",
                                        password=self.password, database=self.db, port=3306, charset='utf8')

    '''+-----------+-----------+------+-----+---------+----------------+
       | Field     | Type      | Null | Key | Default | Extra          |
       +-----------+-----------+------+-----+---------+----------------+
       | name      | char(65)  | YES  |     | NULL    |                |
       | artist    | char(31)  | YES  |     | NULL    |                |
       | keywords  | char(250) | YES  | PRI | NULL    |                |
       | link      | char(250) | NO   |     | NULL    |                |
       | adult     | int(11)   | YES  |     | NULL    |                |
       | downloaded| int(11)   | NO   |     | 0       |                |
       | time      | int(11)   | NO   |     | NULL    |                |
       | owner     | char(31)  | NO   | PRI | NULL    |                |
       +-----------+-----------+------+-----+---------+----------------+
       downloaded default == 0 means not downloaded
       adult == 0 means have no adult content
    '''

    def database_create(self):
        cursor = self.database.cursor()
        order = '''create table if not exists Artwork(
                        name       char(65),
                        artist     char(31),
                        keywords   char(250),
                        link       char(250)  not null,
                        adult      int,
                        downloaded int        Default 0,
                        time       int,
                        owner      char(31),
                        primary key (link,owner)
                        )
                    '''
        cursor.execute(order)
        self.database.close()

    def database_insert(self, results):
        database = pymysql.connect(host=self.host, user="root",
                                   password=self.password, db=self.db, port=3306)
        cursor = database.cursor()
        print(results)
        for result in results:
            insert = ('''insert ignore into artwork(name,artist,keywords,link,adult,time,owner)
                            values
                            ("%s", "%s", "%s", "%s", %d, %d, "%s")''' % (
                result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
            try:
                cursor.execute(insert)
                database.commit()
            except:
                pass
        database.close()

    def database_output(self, owner, switch='***'):
        output = []
        database = pymysql.connect(host=self.host, user="root",
                                   password=self.password, db=self.db, port=3306)
        cursor = database.cursor()
        if switch == '****':
            order = ('''
                        select name,artist,keywords,link,adult,time,owner from artwork where owner = '%s'
                        ''' % owner)
        if not Constant.FAVS:
            order = ('''
                        select link,artist from artwork where owner = '%s' and artist = '%s' and downloaded = 0
                        ''' % (owner, owner))
        else:
            order = ('''
                            select link,artist from artwork where owner = '%s' and artist != '%s' and downloaded = 0
                            ''' % (owner, owner))
        try:
            cursor.execute(order)
            results = cursor.fetchall()
            database.close()

        except:
            print('Fetch error')

        if switch == '****':
            for i in list(results):
                output.append(i)
        else:
            for i in list(results):
                output.append(('http:' + i[0], i[1]))

        return output

    def database_downloaded(self, results):
        database = pymysql.connect(host=self.host, user="root",
                                   password=self.password, db=self.db, port=3306)
        cursor = database.cursor()
        for i in results:
            update = ('''update artwork set downloaded = 1 where link = '%s'
                           ''' % (i[5:]))
            try:
                cursor.execute(update)
                database.commit()
            except:
                print('Update error')
        database.close()

    def database_update(self, owner):
        time_output = []
        database = pymysql.connect(host=self.host, user="root",
                                   password=self.password, db=self.db, port=3306)
        cursor = database.cursor()
        order = ('''
                        select time from artwork where owner = '%s'
                        ''' % owner)
        try:
            cursor.execute(order)
            time_results = cursor.fetchall()
            database.close()

        except:
            print('Fetch error')
        if time_results == ():
            max_update_date = 0  # 1970-1-1
        else:
            for i in list(time_results):
                for k in list(i):
                    time_output.append(k)
            max_update_date = max(time_output)

        return max_update_date, time_output

    def artist_output(self, downloaded=1):
        database = pymysql.connect(host=self.host, user="root",
                                   password=self.password, db=self.db, port=3306)
        cursor = database.cursor()
        order = ('''
                        select distinct artist from artwork where downloaded = %s;
                        ''' % downloaded)
        try:
            cursor.execute(order)
            artists = cursor.fetchall()
            database.close()
        except:
            print('Fetch error')
        return artists

