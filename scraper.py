import requests
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict():
    """
    Функция парсит данные о книге со страницы:
    http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
    
    Собирает всю информацию о книге, включая название, цену, рейтинг, количество в наличии,
    описание и дополнительные характеристики из таблицы Product Information.

    Результат возвращает в виде словаря.
    
    Входной аргумент (str):
        book_url: URL-адрес страницы для парсинга
        
    Возвращаемые значения (dict):
        Словарь с данными о книге, где ключи - названия характеристик,
        значения - соответствующие данные.
    """

    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    book_info = {}
        
    title = soup.find('h1')
    book_info['title'] = title.text if title else ""

    price = soup.select_one('p.price_color')
    book_info['price'] = price.text if price else ""

    rating = soup.find('p', class_='star-rating')
    book_info['rating'] = ""
    if 'One' in rating['class']:
        book_info['rating'] = 1
    if 'Two' in rating['class']:
        book_info['rating'] = 2    
    if 'Three' in rating['class']:
        book_info['rating'] = 3
    if 'Four' in rating['class']:
        book_info['rating'] = 4
    if 'Five' in rating['class']:
        book_info['rating'] = 5

    stock = soup.find('p', class_='availability')
    book_info['stock'] = stock.text.strip() if stock else ""

    desc = soup.find('div', id='product_description')
    description_text = desc.find_next_sibling('p') if desc else None
    book_info['description'] = description_text.text if description_text else ""

    table = soup.find('table', class_='table-striped')
    rows = table.find_all('tr')
    for row in rows:
        name = row.find('th')
        value = row.find('td')
        book_info[name.text] = value.text if value else ""
    
    return book_info

def scrape_books(is_save=False):
    """
    Функция проходится по всем страницам из каталога сайта Books to Scrape.
    И осуществляет парсинг всех страниц в цикле, 
    используя ранее написанную get_book_data.

    Входной аргумент (bool):
        is_save: Аргумент-флаг для сохранения результатов в файл. 
        Если True, информация сохраняется в ту же папку в файл 'books_data.txt'.

    Возвращаемые значения (list):
    Список словарей, с полной информацией о каждой книге с сайта.
    """

    all_books = []
    page_number = 1
    
    while True:
        url = f"http://books.toscrape.com/catalogue/page-{page_number}.html"        
        print(f"Страница {page_number}")        
        page = requests.get(url)        
        if page.status_code == 404:
            break
            
        soup = BeautifulSoup(page.content, 'html.parser')       
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            book_link = book.find('h3').find('a')['href']            
            if book_link.startswith('../../../'):
                book_link = book_link.replace('../../../', '')
            book_url = f"http://books.toscrape.com/catalogue/{book_link}"
            
            book_data = get_book_data(book_url)
            all_books.append(book_data)
            print(f"{book_data['title']}")
        
        next_btn = soup.find('li', class_='next')
        if not next_btn:
            break
            
        page_number += 1
    
    if is_save:
        with open('books_data.txt', 'w', encoding='utf-8') as f:
            for book in all_books:
                for key, value in book.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")
    
    return all_books