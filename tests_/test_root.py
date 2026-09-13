from app import schema
from jose import jwt
from app.config import settings
import pytest


def test_root(client):
    res = client.get("/")
    response = res.json().get("message")
    assert response == "Hello, World!"
    assert res.status_code == 200



@pytest.mark.parametrize("email,password,status_code",[("zaobanbello9@gmail.com","wrongpassword123", 422),
("zaoabanlautech@gmail.com","wrongpassword123",422),
(None,"password123",422),
("zaobanbello@gmail.com",None,422)])
def test_incorrect_login(client, email,password,status_code):
    res = client.post("/login", json={"username": email, "password": password})
    assert res.status_code == status_code

   

