import os

import pytest
import requests

BASE_URL = "https://cryptic-river-21647-7efe93940f14.herokuapp.com/"

book_id = None


def test_post_and_id_with_get_put_remove():
    global book_id
    url = BASE_URL + "books/"

    data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic",
        "publish_year": "1925",
    }
    response = requests.post(
        url, json=data, headers={"Content-Type": "application/json"}
    )

    book_id = response.json()["id"]

    assert response.status_code == 201


def test_get_book_by_id():
    global book_id
    response = requests.get(f"{BASE_URL}books/{book_id}")

    assert response.status_code == 200
    assert response.json()[0]["fields"]["title"] == "The Great Gatsby"
    assert response.json()[0]["fields"]["author"]
    assert response.json()[0]["fields"]["genre"] == "Classic"
    assert response.json()[0]["fields"]["publish_year"] == 1925


def test_put_book_by_id():
    global book_id

    data = {
        "title": "The Great Gatsby 2",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic",
        "publish_year": "1925",
    }
    response = requests.put(
        f"{BASE_URL}books/{book_id}",
        json=data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Book '{data['title']}' has been updated"


def test_remove_book_by_id():
    global book_id
    response = requests.delete(f"{BASE_URL}books/{book_id}")

    assert response.status_code == 200
    assert response.json()["book"] == "'The Great Gatsby 2' has been deleted"


def test_put_book_by_id_deleted():
    global book_id

    data = {
        "title": "The Great Gatsby 2",
        "author": "F. Scott Fitzgerald",
        "genre": "Classic",
        "publish_year": "1925",
    }
    response = requests.put(
        f"{BASE_URL}books/{book_id}",
        json=data,
        headers={"Content-Type": "application/json"},
    )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["Error"] == "Book does not exist"


def test_books_get():
    r = requests.get(BASE_URL + "books/")
    assert r.status_code == 200

    r = requests.get(BASE_URL + "books/?search=The Adventures of Sherlock Holmes")
    assert r.status_code == 200

    r = requests.get(BASE_URL + "books/?search=J")
    assert r.status_code == 200

    r = requests.get(
        BASE_URL + "books/?title=The Adventures of Sherlock Holmes&genre=Novel"
    )
    assert r.status_code == 200

    r = requests.get(
        BASE_URL
        + "books/?title=The Adventures of Sherlock Holmes&author=Arthur Conan Doyle&genre=Novel&publish_year=1892"
    )
    assert r.status_code == 200

    r = requests.get(
        BASE_URL
        + "books/?title=The Adventures of Sherlock Holmes&author=Arthur Conan Doyle&genre=Novel&publish_year=1893"
    )
    assert r.status_code == 404

    r = requests.get(
        BASE_URL + "books/?title=The Adventures of Sherlock Holmes&author=Arthur Conan "
        "Doyle&genre=Novel&publish_year=1892&publish_year=1893"
    )
    assert r.status_code == 404

    r = requests.get(
        BASE_URL
        + "books/?title=The Adventures of Sherlock Holmes&author=Arthur Conan Doyle&genre=Novel&publish_year=1892&publish_year=1892"
    )
    assert r.status_code == 200


def test_books_post():
    body = {
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "genre": "Novel",
        "publish_year": "1892",
    }

    r = requests.post(
        BASE_URL + "books/", json=body, headers={"Content-Type": "application/json"}
    )

    if r.status_code == 400:
        assert r.json()["message"] == "Book already exists"
        assert r.json()["status"] == 400

    elif r.status_code == 201:
        assert r.json()["title"] == body["title"]
        assert r.json()["author"] == body["author"]
        assert r.json()["genre"] == body["genre"]
        assert r.json()["publish_year"] == body["publish_year"]


def test_books_post_invalid_data():
    body = {
        "title": "The Adventures of Sherlock Bomes",
        "author": "Arthur Conan Loyed",
        "genreS": "Loven",
        "publish_year": "1892",
    }

    r = requests.post(BASE_URL + "books/", json=body)
    print(r.json())

    assert r.status_code == 400
    assert r.json()["message"] == "Missing data field. Please, check your input"
    assert r.json()["fields"] == {
        "1": "title",
        "2": "publish_year",
        "3": "author",
        "4": "genre",
    }
    assert r.json()["status"] == 400


def test_url_get_request():
    r = requests.get(BASE_URL)
    assert r.status_code == 200
    print(r.json())
    assert "books" in r.json()
    assert "authors" in r.json()


def test_het_author_by_id():
    r = requests.get(BASE_URL + "authors/1")
    assert r.status_code == 200
    assert r.json()[0]["fields"]["name"] == "F. Scott Fitzgerald"


def test_het_author_by_name():
    r = requests.get(BASE_URL + "authors/?name=F. Scott Fitzgerald")
    assert r.status_code == 200
    assert r.json()[0]["fields"]["name"] == "F. Scott Fitzgerald"


if __name__ == "__main__":
    pytest.main([os.path.realpath(__file__)])
