import pytest
from scraper import get_book_data, scrape_books

def test_get_book_data_returns_dict():
    #Тест: функция возвращает словарь
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    
    assert type(result) == dict
    assert len(result) > 0

def test_get_book_data_fields_are_strings():
    #Тест: основные поля содержат строки
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    
    assert type(result['title']) == str
    assert type(result['price']) == str
    assert type(result['description']) == str

def test_scrape_books_returns_correct_number():
    #Тест: количество собранных книг соответствует ожиданиям
    result = scrape_books(is_save=False)
    
    # На каждой странице 20 книг, тестируем 2 страницы = 40 книг
    assert len(result) == 40
    assert type(result) == list
    assert all('title' in book for book in result)
    