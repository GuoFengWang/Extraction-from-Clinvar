#!/usr/bin/python
# -*- coding: utf-8 -*-

from OrphaNetCrawler.items import OrphanetcrawlerItem
import re
from scrapy.http import Request, FormRequest
from scrapy.spiders import Spider


class OrphaNetSpider(Spider):
    name = 'orphanet'
    allowed_domains = ['orpha.net']
    start_urls = ['https://www.orpha.net/consor/cgi-bin/Disease_Search.php?lng=EN']

    def parse(self, response):
        with open('/Users/Andy/Desktop/OrphaNetCrawler/finall_gene.txt')as file:
            for line in file:
                omim_num = line.split('\t')[0]  # Omim_number
                yield FormRequest.from_response(  # simulate a click on search button
                    response,
                    method='POST',
                    formname='FormName',
                    formdata={
                        'Disease_Disease_Search_diseaseGroup': str(omim_num), 
                         # search content: Orpha Number
                    },
                    clickdata={  # click 'OMIM Number'
                        'name': 'Disease_Disease_Search_diseaseType',
                        'value': 'OMIM'
                    },
                    callback=self.parser_link
                )

    def parser_link(self, response):
        """get URL of search result"""
        urls = response.xpath('//div/div/a[@class="btn-lnk"]/@href').extract()
        if urls:  # has search result
            url = response.urljoin(urls[0])  # Relative URL => Absolute URL
            yield Request(url, method='GET', callback=self.parser_content)

    def parser_content(self, response):
        """parser search content"""
        encode = 'utf-8'  # ISO-8859-1
        items = OrphanetcrawlerItem()

        #Title
        title = response.xpath('/html/head/title/text()').extract_first()
        items['title'] = title.strip()

        #Synonym
        synonym = response.xpath('//*[@id="ContentType"]/div[5]/ul/li[1]/em/following-sibling::ul/li').extract()
        if synonym:
            synonym = list(map(lambda x: re.sub('</?li>|</?strong>', '', x), synonym))
        items['synonym'] = ','.join(synonym)

        # Disease
        #disease = response.xpath('//div[@id="ContentType"]/h2[last()]/text()').extract_first()
        #items['disease'] = disease.encode(encode)

        # Disease definition
        disease_def = response.xpath('//div[@id="ContentType"]/div[@class="definition"]/section/p/text()').extract_first()
        items['disease_def'] = disease_def

        # OrphaNet ID
        #orphanet_id = response.xpath('//div[@id="ContentType"]/div[@class="idcard artBlock"]/h3/text()').extract_first()
        #items['orphanet_id'] = orphanet_id.encode(encode).split(':')[1]

        contents = response.xpath('//div[@id="ContentType"]/div[@class="idcard artBlock"]/ul/li').extract()

        # Prevalence
        #prevalence_r = re.search('<em>Prevalence: </em><strong>(.*)</strong>', contents[1].encode(encode))
        prevalence_r = re.search('<em>Prevalence: </em><strong>(.*)</strong>', contents[1])
        if prevalence_r:
            items['prevalence'] = prevalence_r.group(1)
            if not items['prevalence']:
                items['prevalence'] = '-'
        else:
            items['prevalence'] = '-'

        # Inheritance
        #inheritance_r = re.search('<em>Inheritance: </em><strong>(.*)</strong>', contents[2].encode(encode))
        #if inheritance_r:
            # items['inheritance'] = inheritance_r.group(1)
        #    items['inheritance'] = re.sub('\s+$', '', inheritance_r.group(1))

        #else:
        #    items['inheritance'] = '-'

        # Age of onset
        #onset_age_r = re.search('<em>Age of onset: </em><strong>(.*)</strong>', contents[3].encode(encode))
        onset_age_r = re.search('<em>Age of onset: </em><strong>(.*)</strong>', contents[3])
        if onset_age_r:
            # items['onset_age'] = onset_age_r.group(1)
            items['onset_age'] = re.sub('</?strong>|\s+', '', onset_age_r.group(1))

        else:
            items['onset_age'] = '-'

        # OMIM
        #omim_r = re.search('<em>OMIM: </em><strong><a.*>(.*)</a></strong>', contents[5].encode(encode))
        omim_r = re.search('<em>OMIM: </em><strong><a.*>(.*)</a></strong>', contents[5])
        if omim_r:
            items['omim'] = omim_r.group(1)
        else:
            items['omim'] = '-'




        yield items