from typing import Optional

# uvicorn app.main:app --reload

from fastapi import FastAPI, Response, status, HTTPException  # create api
from fastapi.params import Body  # extract data
from pydantic import BaseModel  # create schema for validation
from random import randrange

app = FastAPI()


class Post(BaseModel):  # pydantic model
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None  # Optional value


my_post = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite food", "content": "I like pizza", "id": 2}
]

message = [
    {"message": "Welcome to my girlfriend house"},
]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


@app.get("/")  # '/' is root path doesn't matter it emitted or not # route in angular
def root():  # function name doesn't matter

    return message


@app.get("/posts")  # https method and path of url # use plural for naming convention
def get_posts():
    return {"data": my_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):  # validation user post data # auto extract data from raw json
    post_dict = post.dict()  # convert model to dict format
    post_dict['id'] = randrange(0, 1000000)  # generate unique id for our posts
    my_post.append(post_dict)  # append to my post array
    return {"data": post_dict}  # send back new post


@app.get("/posts/{id}")
def get_post(id: int):  # validate id parameter
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # don't return more content
def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data": post_dict}
