import requests
from bs4 import BeautifulSoup
import pdfkit
import time
import os

PDF_CONFIG = {
    # 'page-size': 'Letter',
    # 'margin-top': '0.75in',
    # 'margin-right': '0.75in',
    # 'margin-bottom': '0.75in',
    # 'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    # 'no-outline': None
}


def get_data(url):
    headers = {
        'accept': 'text/html,application/xhml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text


# 文章模型
class Article(object):
    title: str
    time: str
    link: str
    content: str


# 获取所有文章列表
def date_convert(date_string):
    formate = time.strptime(date_string, "%Y/%m/%d")
    new_date_string = time.strftime("%Y-%m-%d", formate)
    return new_date_string


def get_articles(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find('ul', attrs={'class': 'featured-post'})
    models = []
    for article in articles:
        model = Article()
        model.link = article.a.get('href')
        model.title = article.a.string
        model.time = date_convert(article.span.string)
        models.append(model)
    return models


def get_article_content(article: Article):
    html = get_data(article.link)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find("article")
    return str(content)


def save_to_pdf(article: Article):
    pdf_name = f'{article.time}={article.title}.pdf'
    try:
        config = pdfkit.configuration()
        pdfkit.from_string(article.content, pdf_name, options=PDF_CONFIG)
    except:
        print(pdf_name + "转换pdf失败")
    finally:
        pass


# 文章列表
def start():
    homepage = 'https://coolshell.cn/featured'
    html = get_data(url=homepage)
    articles = get_articles(html)
    print(f'爬取到{len(articles)}篇')
    for i, article in enumerate(articles):
        pdf_name = f'{article.time}={article.title}.pdf'
        if not os.path.exists(pdf_name):
            article.content = get_article_content(article)
            save_to_pdf(article)
            print(f'爬取第{i}篇: {article.title}')
        else:
            print(f'已爬取过第{i}篇: {article.title}')
    print("爬取完成")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()
