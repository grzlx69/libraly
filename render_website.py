import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from itertools import count
from more_itertools import chunked


with open("books_params.json", "r", encoding="utf-8") as my_file:
    books_params = json.load(my_file)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

os.makedirs('pages', exist_ok=True)
books_on_page = 10
chunked_books = list(chunked(books_params, books_on_page))
total_pages = len(chunked_books)

for number, books_page in enumerate(chunked_books):

    index = env.get_template('template.html')
    rendered_page = index.render(
        books_params = books_page,
        page_number = number+1,
        total_pages = total_pages
    )
    with open(f'pages/index{number+1}.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)




server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()