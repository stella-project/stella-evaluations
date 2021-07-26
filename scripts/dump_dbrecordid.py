from db import *
from util import *
from config import *


def main():

    livivo_id = users.select().where(users.c.username == 'LIVIVO').execute().first().id
    rankings = results.select().where(results.c.site_id == livivo_id).execute().fetchall()

    dbrecordids = set()
    
    for ranking in rankings:
        for rank, doc in ranking[-1].items():
            dbrecordid = doc.get('docid')
            dbrecordids.add(dbrecordid)
            print(dbrecordid)

    with open('dbrecordids.txt', 'w') as f_out:
        for dbrecordid in dbrecordids:
            f_out.write(str(dbrecordid) + '\n')
        
if __name__ == '__main__':
    main()