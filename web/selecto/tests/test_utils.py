import pytest
from products.utils import get_page_title


def test_get_page_title_index():
    assert get_page_title('index') == 'Selecto - Index'

def test_get_page_title_details():
    assert get_page_title('details', 'Product 1') == 'Selecto - Product 1'

def test_get_page_title_review_details():
    assert get_page_title('review_details', 'Product 1') == 'Selecto - Product 1 - Review'

def test_get_page_title_contact_us():
    assert get_page_title('contact_us') == 'Selecto - Contact Us'

def test_get_page_title_about_us():
    assert get_page_title('about_us') == 'Selecto - About Us'

def test_get_page_title_login():
    assert get_page_title('login') == 'Selecto - Log In'

def test_get_page_title_signup():
    assert get_page_title('signup') == 'Selecto - Sign Up'

def test_get_page_title_invalid_input():
    assert get_page_title() == 'Selecto'
    assert get_page_title('invalid_input') == 'Selecto'
    assert get_page_title(1, 2, 3, 4, 5, 6) == 'Selecto'