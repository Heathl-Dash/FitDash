import pytest
from factories import ToDoFactory
from fitCore.models import ToDo

@pytest.mark.django_db
def test_create_todo(auth_client):
    new_todo = ToDoFactory.build()
    payload = {
        "title": new_todo.title,
        "description": new_todo.description,
    }
    response = auth_client.post("/api/v1/fit/todo/", data=payload, format="json")
    assert response.status_code == 201, response.content
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]

@pytest.mark.django_db
def test_delete_todo(auth_client):
    habit = ToDoFactory.create(user_id=1)
    response = auth_client.delete(f"/api/v1/fit/todo/{habit.id}/")
    assert response.status_code == 204, response.content
    with pytest.raises(ToDo.DoesNotExist):
        ToDo.objects.get(id=habit.id)

@pytest.mark.django_db
def test_edit_habit(auth_client):
    todo = ToDoFactory.create(user_id=1)

    updated_data = {
        "title": "Novo título",
        "description": "Nova descrição",
    }

    response = auth_client.patch(f"/api/v1/fit/todo/{todo.id}/", data=updated_data, format="json")
    
    assert response.status_code == 200, response.content

    todo.refresh_from_db()
    assert todo.title == updated_data["title"]
    assert todo.description == updated_data["description"]

@pytest.mark.django_db
def test_list_habit(auth_client):
    ToDoFactory.create_batch(3, user_id=1)  

    response = auth_client.get("/api/v1/fit/todo/")

    assert response.status_code == 200, response.content

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    first = data[0]
    expected_fields = {"id", "title", "description"}
    assert expected_fields.issubset(first.keys())

@pytest.mark.django_db
def test_retrieve_habit(auth_client):
    todo = ToDoFactory.create(user_id=1)

    response = auth_client.get(f"/api/v1/fit/todo/{todo.id}/")

    assert response.status_code == 200, response.content
    data = response.json()

    assert data["title"] == todo.title
    assert data["description"] == todo.description
    assert data["done"] == todo.done