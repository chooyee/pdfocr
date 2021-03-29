from db.sqlite import ConMan 

def GetConList(uuid):
    with ConMan() as con:
        sql = '''select * from conlist where uuid=?'''
        rows = con.Select(sql, (uuid,))
        return rows