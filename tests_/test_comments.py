import pytest
from app import schema



def test_create_comment(client, test_login, test_create_post):
    token = test_login.access_token
    post = test_create_post[0]
    post_id = post["id"]

    # Create a comment
    response = client.post(
        "/comments/",
        json={
            "post_id": post_id,
            "content": "This is a test comment"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["content"] == "This is a test comment"
    assert data["post_id"] == post_id


def test_get_comments(client, test_login, test_create_post):
 
    token = test_login.access_token

    post = test_create_post[0]
    post_id = post["id"]

    response = client.post(
        "/comments/",
        json={
            "post_id": post_id,
            "content": "This is a test comment"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get(
        f"/comments/{post_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()
 
    assert len(data) == 1
    assert data[0]["content"] == "This is a test comment"