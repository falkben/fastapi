from fastapi import Body, BodyOrQuery, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.put("/body_alone/")
async def body_alone(item_id=Body(...)):
    return {"item_id": item_id}


@app.put("/body_query_items/")
async def bodyorquery_only(item_id=BodyOrQuery(...)):
    return {"item_id": item_id}


@app.put("/body_items/")
async def body_and_bodyorquery(item_id=BodyOrQuery(...), body_id=Body("bar")):
    return {"item_id": item_id, "body_id": body_id}


client = TestClient(app)


def test_put_query_arg_body_or_query():
    response = client.put("/body_query_items/?item_id=foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "body_id": "bar"}


def test_put_body_alone():
    response = client.put("/body_alone/", json={"item_id": "foo"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "body_id": "bar"}


def test_put_query_arg():
    response = client.put("/body_items/?item_id=foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "body_id": "bar"}


def test_put_body():
    response = client.put("/body_items/", json={"item_id": "foo"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo", "body_id": "bar"}


def test_put_body_body_or_query():
    response = client.put("/body_query_items/", json={"item_id": "foo"})
    assert response.status_code == 200, response.text
    assert response.json() == {"item_id": "foo"}


def test_put_body_body_or_query_both():
    response = client.put("/body_query_items/?item_id=foo", json={"item_id": "bar"})
    assert response.status_code == 200, response.text
    # TODO: is it foo or bar by default? (look at tornado.get_arguments)
    assert response.json() == {"item_id": "foo"}

