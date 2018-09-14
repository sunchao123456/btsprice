# -*- coding: utf-8 -*-

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
# 
import psycopg2
from pprint import pprint
from bitshares.market import Market
from bitshares.account import Account
from bitshares.asset import Asset
from dateutil.parser import parse
import time
from datetime import datetime, date, timedelta



class TestMain(object): 
    cdatetime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) 
    cdatetime='2018-9-14 16:14:14'
    print((parse(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))- parse(cdatetime)).total_seconds()/(60*60))
     
    # account = Account("magicwallet.witness")
    # print(account.balances)
    CNY=0.705159
    mrate=1.011

    market = Market("BTS:CNY")
    c=market.ticker()['baseSettlement_price']/market.ticker()['latest']
    print(c)
    conn = psycopg2.connect(database="feedprice", user="feedprice", password="Ho5FX3beUd5q9hgTxTJbos9rxTYeds3n", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT id, cvalue,mrate ,createdate from record order by createdate desc limit 2")
    rows = cur.fetchall()

    upline=0
    lowline=0
    cur2=conn.cursor()
    cur2.execute("SELECT id, name, value from params")
    prows = cur2.fetchall()
    for row in prows:
            if row[1]=='upline':
                upline=row[2]
            elif row[1]=='lowline':
                lowline=row[2]
    
    if rows==[]:
        c=c*mrate
    elif rows.__len__()==1:
        c=float(rows[0][1])
        c=c*mrate
        cdatetime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(rows[0][3])) 
    else :
        c=float(rows[0][1])
        if float(rows[0][2])<mrate:
            mrate=mrate*(1+float(upline))
        else:
            mrate=mrate*(1+float(lowline))
        c=c*mrate
         
        cdatetime=rows[0][3].strftime('%Y-%m-%d %H:%M:%S') 

    #start check 
        
    CNY=CNY*c

    sqlinsert="INSERT INTO record (btsprice, feedprice, cvalue,mrate,myfeedprice) \
    VALUES ('"+str(market.ticker()['latest'])+"','"+str(market.ticker()['baseSettlement_price'])+"','"+str(market.ticker()['baseSettlement_price']/market.ticker()['latest'])+"','"+str(mrate)+"','"+str(CNY)+"')"
    cur.execute(sqlinsert)
    conn.commit()
    conn.close()
    print('OK')


    #bitshares = BitShares(node="wss://openledger.hk/ws")
    #
    # conn = psycopg2.connect(database="feedprice", user="feedprice", password="Ho5FX3beUd5q9hgTxTJbos9rxTYeds3n", host="127.0.0.1", port="5432")
    # print("Opened database successfully")
    # cur = conn.cursor()
    # cur.execute('''CREATE TABLE record
    #    (ID INT PRIMARY KEY     NOT NULL,
    #    btsprice        text,
    #    feedprice       text,
    #    cvalue        text,
    #    mrate         text,
    #    myfeedprice   text,
    #    createdate    timestamp with time zone);''') 
    # conn.commit()
    # print ("  successfully");
    # conn.close()