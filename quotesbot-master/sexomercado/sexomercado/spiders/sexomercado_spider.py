import scrapy
import re

class SexomercadoSpiderSpider(scrapy.Spider):
    name = "sexomercado_spider"
    allowed_domains = ["sexomercadobcn.com"]
    start_urls = ["https://www.sexomercadobcn.com/blogs-chicas-escorts-y-agencias-f14.html"]

    def parse(self, response):
        # Extraer los enlaces a los perfiles
        profile_links = response.css('a[href*="-blog-t"]::attr(href)').getall()
        for link in profile_links:
            yield response.follow(link, self.parse_profile)

        # Seguir a la siguiente página
        next_page = response.xpath('//a[contains(@title, "Siguiente Página")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_profile(self, response):
        # Extraer el nombre del título de la página
        title = response.css('title::text').get()
        
        phone_number = None
        
        # Intentar extraer el número de teléfono del título
        phone_match = re.search(r'\b\d{9}\b', title)
        if phone_match:
            phone_number = phone_match.group(0)
        
        # Si no se encuentra en el título, buscar en el cuerpo de la página
        if not phone_number:
            body_text = "".join(response.css('body *::text').getall())
            phone_match = re.search(r'\b\d{9}\b', body_text)
            if phone_match:
                phone_number = phone_match.group(0)

        yield {
            'name': title.split('-')[0].strip(),
            'phone': phone_number,
            'url': response.url
        }
