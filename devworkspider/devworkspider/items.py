# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DevworkspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass
class JobItem(scrapy.Item):
   #thong tin co ban 
    web        = "DevWork"
    tenCV      = scrapy.Field()
    congTy     = scrapy.Field()
    diaDiem    = scrapy.Field()
    skills     = scrapy.Field()
    phucLoi    = scrapy.Field()
    moTa       = scrapy.Field()
    yeuCau     = scrapy.Field()
    linkCongTy = scrapy.Field()

    #thông tin jobOverview
    luong      = scrapy.Field()
    kinhNghiem = scrapy.Field()
    capBac     = scrapy.Field()
    nganhNghe  = scrapy.Field() #loại công việc 
    hinhThuc   = scrapy.Field()
    hanNopCV   = scrapy.Field()
    linkCV     = scrapy.Field()
    soLuong    = scrapy.Field()
    luongTB    = 0