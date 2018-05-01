# coding: utf-8
"""J-Satage抄録収集モジュール."""
from logging import getLogger
from pathlib import Path

from scrapy import Request
from scrapy import Spider

from jstage_spider import abstract_info_extractor as ext

_logger = getLogger(__name__)


class JstageSpider(Spider):
    """J-Stage抄録情報収集用Spider."""
    name = 'jstage'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url_file_path = (
            Path(__file__).parent.parent / 'start_urls.txt'
        ).resolve()
        _logger.debug('load urls from {}'.format(url_file_path))
        with open(url_file_path) as f:
            self.start_urls = [l.rstrip() for l in f if l != '\n']

    def parse(self, response):
        """ページのパース処理を行う."""
        journal_name = response.xpath('/html/head/title/text()').extract_first()
        for li in response.xpath('//ul[@class="search-resultslisting"]/li'):
            yield {
                'id': ext.extract_doi(li),
                'title': ext.extract_title(li),
                'authors': ext.extract_authors(li),
                'abstract_text': ext.extract_abstract_text(li),
                'additional_info': ext.extract_additional_info(li),
                'pdf': ext.extract_pdf_url(li),
                'journal_name': journal_name
            }
        next_pages = response.xpath(
            '//ul[@class="facetsearch-links"]/li/a/@href'
        ).extract()
        for next_page in next_pages:
            yield Request(next_page, callback=self.parse)
