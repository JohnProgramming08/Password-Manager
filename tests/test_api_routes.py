import os


# Upload route
def test_upload_invalid(client):
    test_data = {"sigma": "male", "yup": "nope"}
    response = client.get("upload/67/sigma", json=test_data)

    assert response.status_code == 405


def test_upload_valid(client):
    test_data = {"sigma": "male", "yup": "nope"}
    response = client.post("upload/67/sigma.json", json=test_data)

    assert response.status_code == 200

    os.remove("users/67/sigma.json")
    os.removedirs("users/67")


# Download file route
def test_download_file_invalid1(client):
    response = client.get("/download_file/67/sigma.json")
    assert response.status_code == 405


def test_download_file_invalid2(many_filled_sections_client):
    response = many_filled_sections_client.post("/download_file/67/sigma.json")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {}


def test_download_file_valid(many_filled_sections_client):
    response = many_filled_sections_client.post("/download_file/67/one.json")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"super": "sigma", "iron": "man", "tony": "stark"}


# List sections route
def test_list_sections_invalid(many_filled_sections_client):
    response = many_filled_sections_client.get("/list_sections/test")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {}


def test_list_sections_valid(many_filled_sections_client):
    response = many_filled_sections_client.get("/list_sections/67")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {
        "one.json": "active",
        "two.json": "active",
        "three.json": "active",
    }
