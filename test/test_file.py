import pytest
import requests

# curl -v -H "Content-Type: application/json" --request POST --data "{\"name\": \"Rohit\", \"display_name\": \"voldemort\"}" http://127.0.0.1:8000/create_user/

base_url = 'http://127.0.0.1:8000/'
HEADERS = {
    "content-type": "application/json",
}
user_data = {"name": "Rohit4", "display_name": "Voldemort"}


@pytest.fixture(scope="module")
def user_id():
    url = f"{base_url}/create_user/"
    response = requests.post(base_url, json=user_data, headers=HEADERS)
    assert response.status_code == 200
    id = response.json().get('id')
    print(id)
    return id


def test_create_event():
    assert user_id is not None

# continue...