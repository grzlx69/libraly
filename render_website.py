import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server
import argparse


def on_reload(file_path):
    with open(file_path, "r", encoding="utf-8") as my_file:
        books_params = json.load(my_file)
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    os.makedirs("pages", exist_ok=True)
    books_on_page = 10
    chunked_books = list(chunked(books_params, books_on_page))
    total_pages = len(chunked_books)

    for number, books_page in enumerate(chunked_books):

        index = env.get_template("template.html")
        rendered_page = index.render(
            books_params=books_page, page_number=number + 1, total_pages=total_pages
        )
        with open(f"pages/index{number+1}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(
        description="Эта праграмма загружает данные из json файла, и публикует их на сайт - онлайн-библиотеку."
    )
    parser.add_argument("--path", help="Введите путь к файлу:", default="books_params.json")
    args = parser.parse_args()
    file_path = args.path
    server = Server()
    server.watch("template.html", on_reload(file_path))
    server.serve(root=".", default_filename="./pages/index1.html")


if __name__ == "__main__":
    main()
