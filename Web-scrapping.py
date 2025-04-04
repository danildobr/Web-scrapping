# Домашнее задание к лекции 6. «Web-scrapping»
# Попробуем получать интересующие нас статьи на Хабре самыми первыми.
# Нужно парсить страницу со свежими статьями (https://habr.com/ru/articles/) и выбирать те статьи, в 
# которых встречается хотя бы одно из ключевых слов. Эти слова определяем в начале скрипта. 
# Поиск вести по всей доступной preview-информации, т. е. по информации, доступной с текущей страницы. 
# Выведите в консоль список подходящих статей в формате: <дата> – <заголовок> – <ссылка>.
# Пример preview:
# Шаблон кода:
# Определяем список ключевых слов:
# KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Дополнительное (необязательное) задание
# Улучшите скрипт так, чтобы он анализировал не только preview-информацию статьи, но и весь текст статьи целиком.
# Для этого потребуется получать страницы статей и искать по тексту внутри этой страницы.
import requests
import bs4
from fake_headers import Headers
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def website_article():
    '''Получаем html страницу сайта '''
    respons = requests.get('https://habr.com/ru/articles/', headers=Headers(browser='chrom', os='win').generate())
    # делаем запрос на сайт 
    soup = bs4.BeautifulSoup(respons.text, features='lxml' )
    # помещаем сайт в парссер
    article_list = soup.find_all('article', class_= 'tm-articles-list__item')
    # собираем список статей
    return article_list
    # возвращаем список статей  

def website_parsing(article_list):
    '''Парсим нужную информацияю и формируем вывод'''
    for article in article_list:
        article_url = ('https://habr.com/ru/articles/' + article.get('id')) 
        # формируем url
        article_header = article.find('h2').text 
        # находим заголовок
        article_time = article.find('time')['datetime']
        # находим дату 
        parsed_date = datetime.strptime(article_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        formatted_date = parsed_date.strftime('%d.%m.%Y %H:%M')  
        # формируем красиво дату 
        preview_div = article.find('div', class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
        if preview_div:
            preview_text = preview_div.text.strip()
        else: ""
        # находим preview текст
        has_keyword = any(
        keyword.lower() in article_header.lower() or 
        keyword.lower() in preview_text.lower()
        for keyword in KEYWORDS)
        # проверяем находиться наши ключевые слова в заголовке и preview тексте 
        if article_header and has_keyword:
            print(f'''Дата публикации: {formatted_date}, Заголовок: "{article_header}", Ссылка: {article_url}''')
        # формируем строку 
        
if __name__ == '__main__':
    website_parsing(website_article())
    # вызываем функцию 


