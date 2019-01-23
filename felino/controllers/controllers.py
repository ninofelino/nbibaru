# -*- coding: utf-8 -*-
import thread6
import json
import subprocess
import time
import json
from dbfread import DBF
from odoo import http,exceptions
import re



#import datetime

datalama='/mnt/poserver/ics/DAT/INV.DBF'
class Felino(http.Controller):
      @http.route('/felino/', auth='public')
      def index(self, **kw):
          objects= http.request.env['felino.felino'].search([],limit=30)
          return http.request.render('felino.listing',{'objects':objects})

      @http.route('/felino/dbf', auth='public')
      def list(self, **kw):
          objects= http.request.env['felino.felino'].search([],limit=30)
          threaded_print(objects)  
          return "DBF"
      
      @http.route('/felino/print', auth='public')
      def list(self, **kw):
               
          return "DBF"

      @http.route('/felino/inv', auth='public')
      def inv(self, **kw):
          objects= http.request.env['felino.felino'].search([],limit=30)
          thread6.run_threaded(threaded_inv(objects)).await_output()    
          return "DBF"

      @http.route('/felino/product', auth='public')
      def inv(self, **kw):
          http.request.cr.execute('delete from product_product;delete from product_template;')
          http.request.cr.execute('select * from fi_dbinv order by idx ') 
          data = http.request.cr.fetchall() 
          objects= http.request.env['product.template']
          attr_test= http.request.env['product.attribute'].browse([389])
          print(attr_test.value_ids.ids)
          for record in data:
              px=[]
              attx=[]
              print(record[6])
              attx=record[6]
              #attx=record[5]
              for data in record[5]:
                  px.append((0,0,data))
                  #px.append([0,0,data])
              
              print("------------------------------")
              print(attx)
              print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

              productlist = {'id':record[0],'name':record[1],'list_price':record[3],'standard_price':record[2],
              'product_variant_ids':px,          
              #'attribute_line_ids': [(0, 0, {'attribute_id': 1,'value_ids':[(6, 0,attx)],}),
              'attribute_line_ids': [(0, 0, {'attribute_id': 1,'value_ids':[(4,0,attx)],}),
              
              ] ,
              
              #attribute_value_ids,
              #'qty_availab
              } 
              #try:
              objects.sudo().create(productlist)
              http.request.cr.commit()
              
              #    print('XXXXXXXXXXXXXXXXXXXXXX')
              #    print(productlist.id)
              #    print('XXXXXXXXXXXXXXXXXXXXXX')
                  

              #except Exception:
              #    http.request.cr.rollback()  
                     
              
          return http.request.render('felino.listing')  


      @http.route('/felino/test', auth='public')
      def testinv(self, **kw):
          #objects= http.request.env['felino.inv']
          http.request.cr.execute('select * from felino_felino')    
          data = http.request.cr.fetchall() 
          for record in data:
              print(record[1])   
          
          return "DBF"        

#     @http.route('/felino/felino/objects/<model("felino.felino"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('felino.object', {
#             'object': obj
#         })

      @http.route('/felino/template', auth='public')
      def inv(self, **kw):
          http.request.cr.execute('delete from product_product;delete from product_template;DELETE FROM product_attribute_line')
          http.request.cr.execute('select * from felino_dbinv order by idx  ') 
          data = http.request.cr.fetchall() 
          objects= http.request.env['product.template']
          attr_test= http.request.env['product.attribute'].browse([389])
          print(attr_test.value_ids.ids)
          for record in data:
              catid=record[9]
              if record[9] is None:
                 catid=0
                 
              print("------------------------------")
              print(record[9],record[1])
              print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
              SQL="insert into product_template(tracking,responsible_id,id,name,sequence,type,rental,categ_id,list_price,sale_ok,purchase_ok,uom_id,uom_po_id,company_id,active,default_code,create_uid,write_uid,available_in_pos,create_date)\
               values('none',1,%s,'%s',1,'consu',FALSE,1,%s,TRUE,TRUE,1,1,1,TRUE,'%s',1,1,TRUE,now()) ON CONFLICT ON CONSTRAINT product_template_pkey DO NOTHING"
              http.request.cr.execute(SQL %(record[0],record[1],record[3],record[0]))
              http.request.cr.commit()
              SQL="insert into product_attribute_line(product_tmpl_id,attribute_id) values(\
                  %s,%s) ON CONFLICT DO NOTHING"
              http.request.cr.execute(SQL %(record[0],1) )
              http.request.cr.commit() 
              ls=record[5]
              print(type(ls))
              for isi in ls:
                  print(isi['default_code'])
                  SQL="insert into product_product(id,product_tmpl_id,default_code,active,create_uid,write_uid)\
                  values(%s,%s,'%s',TRUE,1,1) ON CONFLICT DO NOTHING"
                  print(SQL %(int(isi['default_code']),record[0],isi['default_code']))
                  http.request.cr.execute(SQL %(isi['default_code'],record[0],isi['default_code']) )
                  print("----------------kkkk")
                  print(id)
                  http.request.cr.commit()
                  SQL="insert into product_attribute_value_product_product_rel(product_product_id, product_attribute_value_id)\
                  values(%s,%s)"
                  try:
                      http.request.cr.execute(SQL %(isi['default_code'],isi['attribute_value_ids']) )
                  
                      http.request.cr.commit()
                  except:
                      http.request.cr.rollback() 
                  
              #objects.sudo().create(productlist)
              #http.request.cr.commit()
              
              #    print('XXXXXXXXXXXXXXXXXXXXXX')
              #    print(productlist.id)
              #    print('XXXXXXXXXXXXXXXXXXXXXX')
                  

              #except Exception:
              #    http.request.cr.rollback()  
                     
              
          return http.request.render('felino.listing')  
      

def threaded_print(objects):
    product=http.request.env['product.template']
    print("mulai") 
    for item in DBF('/mnt/poserver/ics/DAT/INV.DBF',encoding='iso-8859-1'):
              list=item['DESC1'].split(" ")
              print("start")
              SQL='INSERT INTO felino_felino (barcode,article,name) VALUES (%s,%s,%s) ON CONFLICT ON CONSTRAINT felino_felino_pkey DO NOTHING; '
              #,{"barcode":item['CODE'],"article":article,"ukuran":ukuran}))
              if len(list)>2:
                 ukuran=list[len(list)-1][-2:]
                 article=list[0]+' '+list[1]
                 name=article
                 id=barcode
                 cost=item['COSTPRC']
                 saleprice=item['SELLPRC']
                 barcode=item['CODE']
                 #product.sudo().write({'product_id':item['CODE'],'name':article,'default_code':barcode,'list_price':cost,'lst_price':saleprice,'attribute_line_ids':[{'id':3}]})
                 print(SQL,(barcode,article,name,))
                 http.request.cr.execute(SQL,(barcode,article,name,))
                 http.request.cr.commit()
    return 1
    
def importdbf(objects):
    SQ=''
    current_time = datetime.datetime.now() 
    for item in DBF('/mnt/poserver/ics/DAT/INV.DBF',encoding='iso-8859-1'):
        SQL="insert into felino.felino(id,barcode,article,ukuran,list_prc,sale_price) values(%s,%s,'%s',%s,%s,%s);"
        list=item['DESC1'].split(" ")
        if len(list)>2:
           ukuran=list[len(list)-1][-2:]
           article=list[0]+' '+list[1]
           SQ=SQ+(SQL %(item['CODE'],item['CODE'],article,ukuran,item['COSTPRC'],item['SELLPRC']))
    f = open("result.sql","a")        
    f.write(SQ)
    #print(SQ)   
    print( datetime.datetime.now()-current_time)    
    return 1

def threaded_inv(objects):
    #mulai=time()
    #objects= http.request.env['felino.felino'].search([],limit=30)
    for item in DBF(datalama,encoding='iso-8859-1'):
              list=item['DESC1'].split(" ")
              print(item['DESC1'])
              
              try:
                 ukuran=list[len(list)-1][-2:]
                 article=list[0]+' '+list[1]
                 barcode=item['CODE']
                 cost=item['COSTPRC']
                 saleprice=item['SELLPRC']
                 objects.sudo().create({'id':barcode,'name':article,'article':article,'barcode':barcode,'ukuran':ukuran,'sale_price':saleprice,'list_price':cost})
                 http.request.cr.commit()
              except:
                 print("error")     
   
    return 1    
