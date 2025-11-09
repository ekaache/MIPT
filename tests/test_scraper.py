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

def test_get_book_data_with_different_books():
    """Тест: get_book_data работает с разными книгами и возвращает словари"""
    test_urls = [
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
    ]
    
    for url in test_urls:
        result = get_book_data(url)
        
        assert isinstance(result, dict)
        assert len(result) > 0
        assert 'title' in result
        assert 'price' in result
        
        if url == test_urls[0]:
            title1 = result['title']
        else:
            title2 = result['title']

    assert title1 != title2
    