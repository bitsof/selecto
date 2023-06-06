import pytest
from django.template import Template, Context
from django.core.paginator import Paginator

@pytest.mark.django_db
def test_pagination_links_reviews():
    # Create a dummy paginator with 10 pages
    paginator = Paginator(range(100), 10)

    # Create a dummy page object representing the current page
    page_number = 3
    page_obj = paginator.get_page(page_number)

    # Render the template tag
    template = Template('{% load pagination_tags %}{% pagination_links_reviews page_obj %}')
    context = Context({'page_obj': page_obj})
    rendered = template.render(context)

    # Assert the rendered output
    assert '<div class="pagination justify-content-center mt-3 mb-3">' in rendered
    assert '<span class="step-links">' in rendered
    assert '<a href="?page=1">&laquo; first</a>' in rendered
    assert f'<a href="?page={page_obj.previous_page_number()}">previous</a>' in rendered
    assert f'Page {page_obj.number} of {page_obj.paginator.num_pages}.' in rendered
    assert f'<a href="?page={page_obj.next_page_number()}">next</a>' in rendered
    assert f'<a href="?page={page_obj.paginator.num_pages}"> last &raquo;</a>' in rendered

@pytest.mark.django_db
def test_pagination_links_reviews_no_previous():
    # Create a dummy paginator with 5 pages
    paginator = Paginator(range(50), 10)

    # Create a dummy page object representing the first page
    page_number = 1
    page_obj = paginator.get_page(page_number)

    # Render the template tag
    template = Template('{% load pagination_tags %}{% pagination_links_reviews page_obj %}')
    context = Context({'page_obj': page_obj})
    rendered = template.render(context)

    # Assert the rendered output
    assert '<div class="pagination justify-content-center mt-3 mb-3">' in rendered
    assert '<span class="step-links">' in rendered
    assert '<a href="?page=1">&laquo; first</a>' not in rendered
    assert '<a href="?page=1">previous</a>' not in rendered
    assert f'Page {page_obj.number} of {page_obj.paginator.num_pages}.' in rendered
    assert f'<a href="?page={page_obj.next_page_number()}">next</a>' in rendered
    assert f'<a href="?page={page_obj.paginator.num_pages}"> last &raquo;</a>' in rendered

@pytest.mark.django_db
def test_pagination_links_main():
    # Create a dummy paginator with 10 pages
    paginator = Paginator(range(100), 10)

    # Create a dummy page object representing the current page
    page_number = 3
    page_obj = paginator.get_page(page_number)

    # Render the template tag
    template = Template('{% load pagination_tags %}{% pagination_links_main page_obj %}')
    context = Context({'page_obj': page_obj})
    rendered = template.render(context)

    # Assert the rendered output
    assert '<nav class="d-flex justify-content-center mt-2 mb-2" aria-label="Pages">' in rendered
    assert '<ul class="pagination justify-content-center">' in rendered
    assert '<li class="page-item">' in rendered
    assert f'<a class="page-link" href="?page={page_number - 1}">Previous</a>' in rendered
    assert '<li class="page-item active">' in rendered
    assert f'<a class="page-link" href="?page={page_number}">{page_number}</a>' in rendered
    assert '<li class="page-item">' in rendered
    assert f'<a class="page-link" href="?page={page_number + 1}">Next</a>' in rendered


@pytest.mark.django_db
def test_pagination_links_main_first_page():
    # Create a dummy paginator with 10 pages
    paginator = Paginator(range(100), 10)

    # Create a dummy page object representing the first page
    page_number = 1
    page_obj = paginator.get_page(page_number)

    # Render the template tag
    template = Template('{% load pagination_tags %}{% pagination_links_main page_obj %}')
    context = Context({'page_obj': page_obj})
    rendered = template.render(context)

    # Assert the rendered output
    assert '<nav class="d-flex justify-content-center mt-2 mb-2" aria-label="Pages">' in rendered
    assert '<ul class="pagination justify-content-center">' in rendered
    assert '<li class="page-item disabled">' in rendered
    assert f'<a class="page-link" href="?page={page_number - 1}">Previous</a>' in rendered
    assert '<li class="page-item active">' in rendered
    assert f'<a class="page-link" href="?page={page_number}">{page_number}</a>' in rendered
    assert '<li class="page-item">' in rendered
    assert f'<a class="page-link" href="?page={page_number + 1}">Next</a>' in rendered