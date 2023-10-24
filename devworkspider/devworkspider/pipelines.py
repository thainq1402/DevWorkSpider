# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DevworkspiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Get the field names 
        field_names = adapter.field_names() 

        #list of field that need to strip() the space and '\n'
        strip_field_list = ['tenCV','congTy','diaDiem']
        for item in strip_field_list:
            value = adapter.get(item)
            adapter[item] = value.strip()

        #ETL Kinh Nghiem -> remove 'năm' and strip() the space
        kinh_nghiem_text = 'kinhNghiem'
        value = adapter.get(kinh_nghiem_text)
        value_strip = int(value.replace('năm','').strip())
        adapter[kinh_nghiem_text] = value_strip


        #ETL Han nop CV -> convert to datetime 
        han_nopCV_text = 'hanNopCV'
        value = adapter.get(han_nopCV_text)
        print("===========Type of Han Nop CV=============")
        print(type(value))

        #ETL So luong 
        so_luong_text = 'soLuong'
        value = adapter.get(so_luong_text)
        adapter[so_luong_text] = int(value.replace('người','').strip())

        #ETL Luong
        luong_text = 'luong'
        value = adapter.get(luong_text)
        value_replace = value[0][0].replace('triệu','') # remove text 'triệu' in value 
        #case : 'x-x triệu'
        if len(value_replace) == 2: 
            value_split = value.split('-')
            adapter['luongTB']  = (float(value_split[0]+value_split[1]))/2
        #case : 'Dưới x triệu'
        else: 
            value_split = value_replace.split(' ')
            adapter['luongTB'] = float(value_split[1]) 




        return item
