from typing import Any
import scrapy
from scrapy.http import Response
from devworkspider.items import JobItem


class DevworkSpider(scrapy.Spider):
    name = "devwork"
    allowed_domains = ["devwork.vn"]
    start_urls = ["https://devwork.vn/viec-lam?country=vietnam",
                  "https://devwork.vn/viec-lam?country=japan"
                  ]

    def parse(self, response):
        #function that get the link of each job and go into it then call the parse_dev_work to get the detail of that job
        listing_container = response.css('.listing-container .listing')
        # domain_name = "https://devwork.vn/"            
        for item  in listing_container:
            job_link = item.css('a::attr(href)').get()
            job_link_url = 'https://devwork.vn'+ job_link
            yield response.follow(job_link_url, callback=self.parse_dev_work)


        #next page
        # next_page = response.css('.pagination-item a::attr(href)').get() 
        next_page  = response.css('.pagination-next .pagination-item a::attr(href)').get()           
        if next_page is not None:
            next_page_url = 'https://devwork.vn' + next_page
           
            yield response.follow(next_page_url,callback=self.parse) 
            #request to the next_page_url and then call the function parse 

        pass
    
    def parse_dev_work(self,response):
        ## This method will go into each job and get the detail of each job \
        job_item = JobItem() #intialize the object  jobitem

        block    = response.css('.col-left.col-lg-9')
        block_descs = block.css('.block-desc')

        # class in that page 
        jobOverview = response.css('.widget .job-overview ul') 

        job_item['tenCV']      = response.css('.header-details  h1.mb-3::text').get(),
        job_item['congTy']     = response.css('.header-details h5.mb-10 a::text').get(),
        job_item['linkCongTy'] = 'https://devwork.vn' + response.css('.header-details h5.mb-10 a::attr(href)').get(),
        job_item['diaDiem']    = response.css('.header-details p::text').get(),
        job_item['skills']     = response.css('.col-left.col-lg-9 .tags a::text').getall(),
        #
        job_item['moTa']       = block_descs[0].css('::text').getall(),
        job_item['yeuCau']     = block_descs[1].css('::text').getall(),
        job_item['phucLoi']    = block_descs[3].css('::text').getall(),
        #
        job_item['luong']      = jobOverview.css('ul li:first-child span::text').getall(),
        job_item['kinhNghiem'] = jobOverview.css('ul li:nth-child(2) span::text').get(),
        # job_item['trinhDo']    = jobOverview.css('ul li:nth-child(3) span::text').get(),
        job_item['capBac']     = jobOverview.css('ul li:nth-child(4) span::text').get(),
        job_item['nganhNghe']  = jobOverview.css('ul li:nth-child(5) span::text').get(),
        job_item['hinhThuc']   = jobOverview.css('ul li:nth-child(6) span::text').get(),
        job_item['hanNopCV']   = jobOverview.css('ul li:nth-child(7) span::text').get(),
        job_item['soLuong']    = jobOverview.css('ul li:nth-child(8) span::text').get(),
        job_item['linkCV']     = response.url
        job_item['luongTB']    = 0 

        yield job_item
