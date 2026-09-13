import pytest

@pytest.fixture()
def test_like_post(client, test_login, test_create_post):
    token = test_login.access_token
    post = test_create_post[0]
    post_id = post["id"]
    response = client.post(
            "/vote/",
            json={
                "post_id": post_id,
                "dir": 1
            },
            headers={"Authorization": f"Bearer {token}"}
    )
    return response


def test_like_post_twice(client,test_login,test_like_post,test_create_post):
    token = test_login.access_token
    post = test_create_post[0]
    post_id = post["id"]
    response = client.post(
            "/vote/",
            json={
                "post_id": post_id,
                "dir": 1
            },
            headers={"Authorization": f"Bearer {token}"})
    assert response.status_code ==  409











def test_delete_like(client,test_login,test_like_post,test_create_post):
    token = test_login.access_token
    post = test_create_post[0]
    post_id = post["id"]
    response = client.post(
            "/vote/",
            json={
                "post_id": post_id,
                "dir": 0
            },
            headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    