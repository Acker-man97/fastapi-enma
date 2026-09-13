from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app import schema
from jose import jwt


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Base.metadata.create_all(bind=engine)


TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
 

@pytest.fixture(autouse=True)
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()





@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_create_user(client):
    data = {
        "email": "zaobanbello9@gmail.com",
        "password": "password123"
    }
    res = client.post("/users/", json=data)
    new_user = schema.UserResponse(**res.json())
    assert new_user.email == data["email"]
    return new_user


@pytest.fixture()
def test_login(client, test_create_user):
    data = {
            "username": "zaobanbello9@gmail.com",
            "password": "password123"
        }
    res = client.post("/login",data=data)
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")
    assert user_id == test_create_user.id
    return login_res




@pytest.fixture()
def test_create_post(client, test_login):
    posts_data = [
        {
            "title": "first title",
            "content": "first content"
        },
        {
            "title": "2nd title",
            "content": "2nd content"
        },
        {
            "title": "3rd title",
            "content": "3rd content"
        }
    ]

    token = test_login.access_token
    created_posts = []

    for post in posts_data:
        response = client.post(
            "/posts/",
            json={
                "title": post["title"],
                "content": post["content"],
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        created_posts.append(response.json())

    return created_posts
   