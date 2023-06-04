from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def pagination_links_reviews(page_obj):
    '''
    Turn this section of html code into a template tag that is of the format {% pagination_links_reviews page_obj%}
    <div class="pagination justify-content-center mt-3 mb-3">
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}

            <span class="current-page">
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
            </span>

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </span>
    </div>
    '''
    html = '<div class="pagination justify-content-center mt-3 mb-3"><span class="step-links">'
    
    if page_obj.has_previous():
        html += '<a href="?page=1">&laquo; first</a>\n'
        html += '<a href="?page={}">previous</a>\n'.format(page_obj.previous_page_number())

    html += '<span class="current-page">'
    html += ' Page {} of {}. '.format(page_obj.number, page_obj.paginator.num_pages)
    html += '</span>'

    if page_obj.has_next():
        html += '<a href="?page={}">next</a>\n'.format(page_obj.next_page_number())
        html += '<a href="?page={}"> last &raquo;</a>'.format(page_obj.paginator.num_pages)

    html += '</span></div>'
    
    return format_html(html)

@register.simple_tag
def pagination_links_main(page_obj):
    '''
    Turn this section of html code into a template tag that is of the format {% pagination_links_main page_obj%}
    <nav class="d-flex justify-content-center mt-2 mb-2" aria-label="Pages">
        <ul class="pagination justify-content-center">
            <li class="page-item {% if page_obj.number == 1 %}disabled{% endif %}">
                <a class="page-link" href="?page={{ page_obj.number|add:"-1" }}">Previous</a>
            </li>
            {% for num in page_obj.paginator.page_range %}
                <li class="page-item {% if num == page_obj.number %}active{% endif %}">
                    <a class="page-link" href="?page={{ num }}">{{ num }}</a>
                </li>
            {% endfor %}
            <li class="page-item {% if page_obj.number == page_obj.paginator.page_range|last %}disabled{% endif %}">
                <a class="page-link" href="?page={{ page_obj.number|add:"1" }}">Next</a>
            </li>
        </ul>
    </nav>
    '''
    html = '<nav class="d-flex justify-content-center mt-2 mb-2" aria-label="Pages"><ul class="pagination justify-content-center">'
    
    if page_obj.number == 1:
        html += '<li class="page-item disabled">'
    else:
        html += '<li class="page-item">'
    html += '<a class="page-link" href="?page={}">Previous</a></li>'.format(page_obj.number - 1)

    for num in page_obj.paginator.page_range:
        if page_obj.number == num:
            html += '<li class="page-item active">'
        else:
            html += '<li class="page-item">'
        html += '<a class="page-link" href="?page={}">{}</a></li>'.format(num, num)

    if page_obj.number == page_obj.paginator.num_pages:
        html += '<li class="page-item disabled">'
    else:
        html += '<li class="page-item">'
    html += '<a class="page-link" href="?page={}">Next</a></li>'.format(page_obj.number + 1)

    html += '</ul></nav>'

    return format_html(html)