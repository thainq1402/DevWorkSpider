# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class DevworkspiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        '''
        Variable note:
            value : get the content of item # value = adapter['tenCV']
            value_string : convert content to string type
            value_strip : store the value that was striped 
            value_num : store the number get from string
        '''
        # Get the field names 
        field_names = adapter.field_names() 

        #region Bugs
        #list of field that need to strip() the space and '\n' 
        # ## OK
        # strip_field_list = ['tenCV','congTy','diaDiem']
        # for item in strip_field_list:
        #     value = adapter.get(item)
        #     adapter[item] = value[0].strip()
        #endregion
        #region ETL TenCV: OK
        tenCV_text = 'tenCV'
        value = adapter[tenCV_text]
        adapter[tenCV_text] = value[0].strip()
        #endregion
        #region ETL diaDiem: OK
        diaDiem_text = 'diaDiem'
        value = adapter.get(diaDiem_text)
        adapter[diaDiem_text] = value[0].strip()
        #endregion 
        #region ETL congTy: OK 
        
        #ETL CongTy
        ##OK
        congTy_text = 'congTy'
        value = adapter.get(congTy_text)
        adapter[congTy_text] = value[0].strip()
    #endregion 
        #region ETL kinhNghiem: OK 
        #ETL Kinh Nghiem -> remove 'năm' and strip() the space -> convert to int 
        kinhNghiem_text = 'kinhNghiem'
        value = adapter.get(kinhNghiem_text)
        value_number = re.findall(r'\d+',value[0]) # value_number is a list
        if len(value_number) > 0:
            adapter[kinhNghiem_text] = int(value_number[0])
    #endregion
        #region ETL hinhThuc: OK 
       
        hinhThuc_text = 'hinhThuc'
        value = adapter.get(hinhThuc_text)
        adapter[hinhThuc_text]=value[0]
    #endregion 
        #region ETL moTa: OK     
       
        moTa_text = 'moTa'
        value = adapter.get(moTa_text)
        adapter[moTa_text] = value[0]
    #endregion 
        #region ETL yeuCau: n't Done    
        yeuCau_text = 'yeuCau'
        value = adapter.get(yeuCau_text)
        adapter[yeuCau_text] = value[0]
    #endregion 
        #region ETL HanopCV: OK
        #ETL Han nop CV -> convert to datetime 
        hanNopCV = 'hanNopCV'
        value = adapter.get(hanNopCV)
        adapter[hanNopCV] = value[0]
    #endregion 
        #region ETL soLuong: OK   
        soLuong_text = 'soLuong'
        value = adapter.get(soLuong_text)
        adapter[soLuong_text] = int(value[0].replace('người','').strip())\
        #endregion 
        #region ETL linkCongTy: OK  
        #ETL linkCongTy 
        linkCongTy = 'linkCongTy'
        value = adapter.get(linkCongTy)
        adapter[linkCongTy] = value[0]
        #endregion
        #region ETL capBac: OK   
        capBac_text = 'capBac'
        value = adapter.get(capBac_text)
        adapter[capBac_text] = value[0].strip()
        #endregion
        #region ETL luongTB: OK      
        luong_text = 'luong'
        value = adapter.get(luong_text)
        value_num =re.findall(r'\d+',value[0][0])
        if len(value_num)  > 1 :
            adapter['luongTB'] = 0.5*(float(value_num[0])+float(value_num[1]))
        elif len(value_num) == 1:
            adapter['luongTB'] = float(value_num[0])
        #endregion
        #region ETL skill:
        #endregion
        #region luong:
        luong_text = 'luong'
        value = adapter.get(luong_text)
        adapter[luong_text] = value[0]
        #endregion 
        return item


import mysql.connector

class DataToMySQLPipeline:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host = '103.200.22.212',
                user = 'dulieutu',
                password = ':EHr0H1o5.Pro2',
                database = 'dulieutu_TTTuyenDung'
            )
            #Buoc 1: Create a cursor
            self.cur = self.conn.cursor()
            #Buoc 2: Create table if none exist 
            self.cur.execute(
                """
                Create table if not exists Stg_DevWork_Job(
                
                web varchar(15),
                tenCV varchar(300),
                congTy varchar(300),
                linkCongTy varchar(200),
                linkCV varchar(200),
                diaDiem varchar(500),
                skills varchar(100),
                moTa text,
                yeuCau text,
                phucLoi text,
                luong varchar(100),
                luongTB Decimal(5,2),
                kinhNghiem Decimal(5,2),
                capBac varchar(50),
                nganhNghe varchar(50),
                hinhThuc varchar(70),
                hanNopCV varchar(10),
                soLuong int
            
                )
                """
        )
        except Exception as e:
            print(f"================1.Exeption in creating table : {e}================")

    def process_item(self, item, spider):
        #define the insert statement
        try: 
            self.cur.execute(
            """
            insert  into Stg_DevWork_Job (
            web, tenCV, congTy, linkCongTy, diaDiem, skills, moTa,
            yeuCau, phucLoi, luong, luongTB, kinhNghiem, capBac,
            nganhNghe, hinhThuc, hanNopCV, soLuong, linkCV
            ) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(str(item['web']),str(item['tenCV']),str(item['congTy']),str(item['linkCongTy']),str(item['diaDiem']),str(item['skills']),str(item['moTa']),
                str(item['yeuCau']),str(item['phucLoi']),str(item['luong']),str(item['luongTB']),str(item['kinhNghiem']),str(item['capBac']),str(item['nganhNghe']),str(item['hinhThuc']),
                str(item['hanNopCV']), str(item['soLuong']),str(item['linkCV'])
                )
            )
            ## Execute insert of data into database
            self.conn.commit()
        except Exception as e:
            print(f"================ 2.Exeption in inserting data into tables {e} ================")

        return item
    def close_spider(self,spider):
        ## Close the cursor & connection to database
        self.cur.close()
        self.conn.close()