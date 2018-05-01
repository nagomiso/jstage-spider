# coding: utf-8
"""抄録情報抽出モジュール."""
from logging import getLogger
from re import sub as resub

from w3lib import html

_logger = getLogger(__name__)

REMOVE_STRING = '<a href="javascript:void(0);" '\
                'class="bluelink-style fontsize12 '\
                'full-abstract">抄録全体を表示</a>'
BLANK_PATTERN = r'[\t\r\n]+'


def extract_title(li):
    """タイトルを抽出する."""
    return remove_blank(
        li.xpath(
            'div[@class="searchlist-title"]/a/text()'
        ).extract_first()
    )


def extract_authors(li):
    """著者名を抽出する."""
    authors_string = li.xpath(
        'div[@class="searchlist-authortags customTooltip"]/text()'
    ).extract_first()
    return [author.strip() for author in authors_string.split(',')]


def extract_doi(li):
    """DOIを抽出する."""
    return li.xpath(
        'div[@class="searchlist-doi"]/a/@href'
    ).extract_first()


def extract_abstract_text(li):
    """概要文を抽出する."""
    abstract_text = li.xpath(
        './/div[@class="inner-content abstract"]'
    ).extract_first()
    if isinstance(abstract_text, str):
        abstract_text = abstract_text.replace(
            REMOVE_STRING, '')
        return remove_blank(
            html.remove_tags(abstract_text))
    else:
        return None


def extract_additional_info(li):
    """付属情報を抽出する."""
    additional_info = li.xpath(
        'div[@class="searchlist-additional-info"]'
    ).extract_first()
    return remove_blank(
        html.remove_tags(additional_info))


def extract_pdf_url(li):
    """PDFのURLを抽出する."""
    return li.xpath(
        './/div[@class="lft"]/span/a/@href'
    ).extract_first()


def remove_blank(text):
    """空白文字を除去する."""
    return resub(
        BLANK_PATTERN, '', text
    ).replace('\u2003', ' ').replace('\u3000', ' ').strip()
