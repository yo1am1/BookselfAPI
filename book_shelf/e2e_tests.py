import os

import pytest
import requests

BASE_URL = "https://boiling-dusk-49835-df388a71925c.herokuapp.com/"


@pytest.mark.xfail
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


def test_get_put_delete():
    response = requests.get(f"{BASE_URL}books/{book_id}")

    assert response.status_code == 200
    print(response.json()[0])
    assert response.json()[0]["fields"]["title"] == "The Great Gatsby"
    assert (
        response.json()[0]["fields"]["author"]
        == "(<Author: F. Scott Fitzgerald>, False)"
    )
    assert response.json()[0]["fields"]["genre"] == "Classic"
    assert response.json()[0]["fields"]["publish_year"] == 1925

    data = {
        "title": "The Great Gatsby 2",
        "author": "F. Scott Fitzgerald 2",
        "genre": "Classic 2",
        "publish_year": 19252,
    }
    response = requests.put(
        f"{BASE_URL}books/{book_id}",
        json=data,
        headers={"Content-Type": "application/json"},
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Book 'The Great Gatsby 2' has been updated"
    assert response.json()["updated_fields"] == [
        "title",
        "publish_year",
        "author",
        "genre",
    ]

    response = requests.delete(
        f"{BASE_URL}books/{book_id}", headers={"Content-Type": "application/json"}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["book"] == "'The Great Gatsby 2' has been deleted"
    assert response.json()["status"] == 200


def test_books_get():
    r = requests.get(BASE_URL + "books/")
    assert r.status_code == 200

    r = requests.get(BASE_URL + "books/?title=The Adventures of Sherlock Holmes")
    assert r.status_code == 200

    r = requests.get(
        BASE_URL + "books/?title=The Adventures of Sherlock Holmes&author=J"
    )
    assert r.status_code == 404

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
        BASE_URL
        + "books/?title=The Adventures of Sherlock Holmes&author=Arthur Conan Doyle&genre=Novel&publish_year=1892&publish_year=1893"
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


if __name__ == "__main__":
    pytest.main([os.path.realpath(__file__)])
