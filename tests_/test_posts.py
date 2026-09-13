import pytest
from app import schema




def test_get_post(client, test_login, test_create_post):

    token = test_login.access_token

    latest_post = test_create_post[-1]
    post_id = latest_post["id"]

    response = client.get(f"/posts/{post_id}",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    data = response.json()
    assert data["Posts"]["id"] == post_id
    assert data["Posts"]["title"] == latest_post["title"]


def test_get_all_posts(client, test_create_post, test_login):
    token = test_login.access_token

    response = client.get("/posts/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_create_post)
    

@pytest.mark.parametrize("title, content, published", [
("awesome new title", "awesome new content", True),
("favorite pizza", "i love pepperoni", False),
("tallest skyscrapers", "wahoo", True),])
def test_create_post(client, test_login,test_create_user, title, content, published):
    token = test_login.access_token
    res = client.post("/posts/", json={"title": title, "content": content,
"published": published},headers={"Authorization": f"Bearer {token}"})
    created_post = schema.Response( ** res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_create_user.id


def test_published_default(client, test_login,test_create_user):
    token = test_login.access_token
    res = client.post("/posts/", json={"title": "life's good", "content": "Somewhere in Helsinki"
},headers={"Authorization": f"Bearer {token}"})
    created_post = schema.Response( ** res.json())
    assert res.status_code == 201
    assert created_post.title == "life's good"
    assert created_post.content == "Somewhere in Helsinki"
    assert created_post.published == True
    assert created_post.owner_id == test_create_user.id



def test_unauthorized_published_default(client):
    
    res = client.post("/posts/", json={"title": "life's good", "content": "Somewhere in Helsinki"
},headers={"Authorization": f"Bearer token"})
    assert res.status_code == 401


def test_delete_post(client, test_login,test_create_post):
    token = test_login.access_token
    res = client.delete(f"/posts/{test_create_post[0]['id']}",headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204


def test_delete_not_exist_post(client, test_login,test_create_post):
    token = test_login.access_token
    res = client.delete(f"/posts/99",headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404




def test_update_post(client, test_login, test_create_post):
    token = test_login.access_token
    post = test_create_post[0]
    post_id = post["id"]
    print(post_id)
    data = {
"title": "updated title",
"content": "updatd content",
"id": post_id}
    
    res = client.put(f"/posts/{post_id}", json=data,headers={"Authorization": f"Bearer {token}"})    
    assert res.status_code == 200
    updated_post = schema.Posts(**res.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.published == True