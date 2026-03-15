import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    # create a post
    response = authorized_client.get("/posts/")
    print(response.json())
    def validate(post):
        return schemas.PostOut(**post)
    
    posts = [validate(post) for post in response.json()]
    posts_list = [schemas.PostOut(**post) for post in response.json()]
    assert len(posts) == len(test_posts)    
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert response.status_code == 200

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/9999")
    assert response.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("New Post", "Content of the new post", True),
    ("Another Post", "Content of another post", False),
    ("Third Post", "Content of the third post", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post('/posts/', json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    

def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post('/posts/', json={"title": "Default Published Post", "content": "Content of the default published post"})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == "Default Published Post"
    assert created_post.content == "Content of the default published post"
    assert created_post.published == True
    
def test_unauthorized_user_create_post(client, test_user):
    response = client.post('/posts/', json={"title": "Unauthorized Post", "content": "Content of the unauthorized post"})
    assert response.status_code == 401
    
def test_create_post_missing_fields(authorized_client, test_user):
    response = authorized_client.post('/posts/', json={"title": "Missing Content Post"})
    assert response.status_code == 422

def test_create_post_wrong_data_types(authorized_client, test_user):
    response = authorized_client.post('/posts/', json={"title": 123, "content": True})
    assert response.status_code == 422

def test_create_post_extra_fields(authorized_client, test_user):
    response = authorized_client.post('/posts/', json={"title": "Extra Fields Post", "content": "Content of the extra fields post", "extra_field": "This should be ignored"})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == "Extra Fields Post"
    assert created_post.content == "Content of the extra fields post"

# TODO -> To reimplement logic for empty post title and content
# def test_create_post_empty_title(authorized_client, test_user):
#     response = authorized_client.post('/posts/', json={"title": "", "content": "Content with empty title"})
#     assert response.status_code == 201
    
# def test_create_post_empty_content(authorized_client, test_user):
#     response = authorized_client.post('/posts/', json={"title": "Empty Content Post", "content": ""})
#     assert response.status_code == 201

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_non_existent(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f'/posts/9999999')
    assert response.status_code == 404

def test_delete_post_wrong_user(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert response.status_code == 403

def test_update_post_partial(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
    }
    response = authorized_client.patch(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 200
    updated_post = schemas.PostResponse(**response.json())
    assert updated_post.title == data["title"]
    
def test_update_post_partial_no_body(authorized_client, test_user, test_posts):
    data = {}
    response = authorized_client.patch(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 400

def test_update_post_full(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }
    response = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 200
    updated_post = schemas.PostResponse(**response.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    
def test_update_post_full_no_body(authorized_client, test_user, test_posts):
    data = {}
    response = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 422

def test_update_post_full_incomplete_body(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
    }
    response = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 422

def test_update_post_partial_wrong_user(authorized_client, test_user, test_posts):
    data = {
        "title": "title to update"
    }
    response = authorized_client.patch(f'/posts/{test_posts[3].id}', json=data)
    assert response.status_code == 403

def test_update_post_full_wrong_user(authorized_client, test_user, test_posts):
    data = {
        "title":"title to update",
        "content": "content of the post"
    }
    response = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert response.status_code == 403

def test_update_non_existent_posts_full(authorized_client, test_user, test_posts):
    data = {
        "title":"title to update",
        "content": "content of the post"
    }
    response = authorized_client.put(f'/posts/{99929292}', json=data)
    assert response.status_code == 404
    
def test_update_post_parital_non_existent(authorized_client, test_user, test_posts):
    data = {
        "title":"title to update",
    }
    response = authorized_client.patch(f'/posts/{99929292}', json=data)
    assert response.status_code == 404