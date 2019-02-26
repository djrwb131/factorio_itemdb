import sqlite3 as sql
filename='itemdb.s3db'
class itemdb():
    def __init__(self,filename):
        self.conn = sql.connect(filename)
        self.c = self.conn.cursor()


    def getAllItemNames(self):
        self.c.execute('SELECT name FROM item;')
        return list(x[0] for x in self.c.fetchall())


    def getItemNameByID(self,iid):
        self.c.execute('SELECT name FROM item WHERE id=?;',(int(iid),))
        r=self.c.fetchall()
        if r:
            return r[0]
        return None


    def getItemTime(self,item):
        if type(item) == str:
            self.c.execute('SELECT time FROM item WHERE name LIKE ?;',item)
        else:
            self.c.execute('SELECT time FROM item WHERE id=?;',item)
        r=self.c.fetchall()
        if r:
            return int(r[0][0])
        return None            
        
    
    def getItemRequirements(self,item):
        if type(item) == str:
            self.c.execute(
                '''
                SELECT * FROM item AS i
                LEFT JOIN item_item_requirements AS iir \
                ON i.id = iir.reqID \
                LEFT JOIN item AS si ON si.name LIKE ? \
                WHERE iir.itemID = si.id ;
                ''',
                (item,)
                )
        else:
            self.c.execute(
                '''
                SELECT * FROM item AS i \
                LEFT JOIN item_item_requirements AS iir \
                ON i.id = iir.reqID \
                WHERE iir.itemID = ? ;
                ''',
                (item,)
                )
            
        d=self.c.fetchall()
        return d
    
db=itemdb(filename)
