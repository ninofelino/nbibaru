import datetime
import json
from sqlalchemy import *
import psycopg2
import datetime
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from dbfread import DBF
#sudo mount.cifs //192.168.1.254/posserver /mnt/poserver share -o user=nuansa,password=nuansa,vers=2.1

# tidak tampil menu
# DELETE FROM ir_attachment WHERE url LIKE '/web/content/%';
engine = create_engine("postgresql://felino:felino@localhost/ninofelino")
con = engine.connect() 
conn = psycopg2.connect("postgresql://felino:felino@localhost/ninofelino")
cur = conn.cursor()
cur.execute("delete from felino_felino;")
SQ=''
uk=['ALL','01','2','3','4','5','O','S','M','L','XL','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']
X=0
print(type(uk))
#for u in uk:
    #SQL="insert into product_attribute_value(id,name,attribute_id,create_uid,write_uid) values(%s,'%s',%s,%s,%s) ON CONFLICT ON CONSTRAINT product_attribute_value_pkey DO NOTHING;"
    #cur.execute(SQL %(X,u,1,1,1))
    #print(SQL %(X,u,1,1,1))
    #conn.commit()
    #X=X+1
err=''    
current_time = datetime.datetime.now() 
for item in DBF('/mnt/poserver/ics/DAT/INV.DBF',encoding='iso-8859-1'):
    SQL="insert into felino_felino(id,barcode,article,ukuran,list_prc,sale_price,index,onhand,catagory,description) values(%s,'%s','%s','%s',%s,%s,%s,%s,'%s','%s') ON CONFLICT ON CONSTRAINT felino_felino_pkey DO NOTHING;"
   
    list=item['DESC1'].split(" ")
    article= article=item['DESC1'].replace("'"," ")
    index=0;
    ukuran=''
    for lst in list:
        for u in uk :
            if lst==u:
               #print(item['DESC1'])
               #print(list.index(lst))  
               ukuran=lst
               #print(ukuran)
               print("-------------------")
               print(list)
               index=uk.index(u)
               list.pop(list.index(lst))
               print(list)
               article=''
               for ls in list:
                   article=article+' '+ls
                   print(article)
                  

    
      
    article=article.replace("'"," ")
    ukuran=ukuran.replace("'"," ")
       
    try:
       cur.execute(SQL %(item['CODE'],item['CODE'],article,ukuran,item['COSTPRC'],item['SELLPRC'],index,item['LQOH'],item['MCLSCODE'],item['DESC1']))
       conn.commit()
    except :
       print("ERROR")
       conn.rollback()   
       err=err+(SQL %(item['CODE'],item['CODE'],article,ukuran,item['COSTPRC'],item['SELLPRC'],index,item['LQOH'],item['MCLSCODE'],item['DESC1']))
       
    #SQ=SQ+(SQL %(item['CODE'],item['CODE'],article,ukuran,item['COSTPRC'],item['SELLPRC'],index))
    #print(SQL  %(item['CODE'],item['CODE'],article,ukuran,item['COSTPRC'],item['SELLPRC'],index) )
f = open("err.log","a")        
f.write(err)
print(SQ)