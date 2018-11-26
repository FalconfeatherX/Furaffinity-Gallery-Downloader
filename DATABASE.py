# -*- coding: utf-8 -*-
import pymysql
import Constant

class Database():
    def __init__(self):
        self.password = Constant.PASSWORD
        self.db       = Constant.DB
        self.database = pymysql.connect(host="localhost",user="root",
        password=self.password,db=self.db,port=3306)

    '''+-----------+-----------+------+-----+---------+----------------+
       | Field     | Type      | Null | Key | Default | Extra          |
       +-----------+-----------+------+-----+---------+----------------+
       | id        | int(11)   | NO   | PRI | NULL    | auto_increment |
       | name      | char(50)  | YES  |     | NULL    |                |
       | artist    | char(15)  | YES  |     | NULL    |                |
       | keywords  | char(150) | YES  |     | NULL    |                |
       | link      | char(120) | NO   | UNI | NULL    |                |
       | adult     | int(11)   | YES  |     | NULL    |                |
       | downloaded| int(11)   | NO   |     | 0       |                |
       +-----------+-----------+------+-----+---------+----------------+
       downloaded default = 0 means not downloaded
       adult = 0 means have no adult content
    '''

    def databaseCreate(self):
        cursor = self.database.cursor()
        order = '''create table if not exists Artwork(
                    id         int        not null PRIMARY KEY auto_increment,
                    name       char(50),
                    artist     char(31),
                    keywords   char(150),
                    link       char(120)  not null UNIQUE KEY,
                    adult      int,
                    downloaed  int        Default 0
                    )
                '''
        cursor.execute(order)
        self.database.close()


    def databaseinsert(self,results):
        database = pymysql.connect(host="localhost",user="root",
        password=self.password,db=self.db,port=3306)
        cursor = database.cursor()
        for result in results:
            insert = ('''insert ignore into Artwork(name,artist,keywords,link,adult)
                        values
                        ("%s","%s","%s","%s",%d)'''%(result[0],result[1],result[2],result[3],result[4]))
            try:
                cursor.execute(insert)
                database.commit()
            except:
                print('echo data detected')
        database.close()


    def databaseoutput(self,artist):
        output = []
        database = pymysql.connect(host="localhost",user="root",
        password=self.password,db=self.db,port=3306)
        cursor = database.cursor()
        order = ('''
                select link from artwork where artist = '%s' and downloaded = 0
                '''%(artist))
        try:
            cursor.execute(order)
            results = cursor.fetchall()
            database.close()
            for i in list(results):
                for k in list(i):
                    output.append('http:' + k)
        except :
            print('Fetch error')
        return output

    def databasedownloaded(self,results):
         database = pymysql.connect(host="localhost",user="root",
         password=self.password,db=self.db,port=3306)
         cursor = database.cursor()
         for i in results:
             update = ('''update artwork set downloaded = 1 where link = '%s'
                       '''%(i[5:]))
             try:
                 cursor.execute(update)
                 database.commit()
             except:
                 print('Update error')
         database.close()
