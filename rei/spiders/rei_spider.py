import scrapy
import json
import re
class ReiSpiderSpider(scrapy.Spider):
    name = 'rei_spider'

    custom_settings = {
		'FEEDS': {
			'rei.csv': {
				'format': 'csv',
				'encoding': 'utf-8-sig',
				'overwrite': True,
			},
		},
	}
    
    
    def start_requests(self):
    
        
        url='https://www.rei.com/sitemap.xml'
        yield scrapy.Request(url=url, callback=self.parse_xml)
    def parse_xml(self,response):
        
        
        links=re.findall('loc>(.+product.+)<\/loc',response.text)
        for link in links:
            yield scrapy.Request(url=link, callback=self.get_products_links)
    def get_products_links(self,response):
        
        
        
        
        links=re.findall('loc>(.+product.+)<\/loc',response.text)
        for link in links:
            print(link)
            yield scrapy.Request(url=link, callback=self.scrape_product)
        
    def scrape_product(self,response):
        
        product_data=response.xpath('//script[@type="application/ld+json"][contains(text(),"Product")]/text()').get()
        if product_data:
            product_data = json.loads(product_data)

            item = {
                'id': product_data.get('@id'),
                'name': product_data.get('name'),
                'image': product_data.get('image'),
                'description': product_data.get('description'),
                'url': product_data.get('url'),
                'sku': product_data.get('sku'),
                'category': product_data.get('category'),
                'weight': product_data.get('weight'),
                'color': ', '.join(product_data.get('color', [])),
                'brand_name': product_data.get('brand', {}).get('name'),
                'brand_image': product_data.get('brand', {}).get('image'),
                'brand_url': product_data.get('brand', {}).get('url'),
                'price': product_data.get('offers', [{}])[0].get('price'),
                'price_currency': product_data.get('offers', [{}])[0].get('priceCurrency'),
                'item_condition': product_data.get('offers', [{}])[0].get('itemCondition'),
                'seller': product_data.get('offers', [{}])[0].get('seller', {}).get('name'),
                'availability': product_data.get('offers', [{}])[0].get('availability'),
                'rating_value': product_data.get('aggregateRating', {}).get('ratingValue'),
                'review_count': product_data.get('aggregateRating', {}).get('reviewCount'),
                # 'gtin13': ', '.join(product_data.get('gtin13', [])),
            }

            yield item