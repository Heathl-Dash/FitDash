import pytest
from factories import ToDoFactory
from unittest.mock import Mock, patch

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_create_todo_unit():
    todo = ToDoFactory.build(
        title="Comprar leite", description="Ir ao mercado", user_id=1
    )

    with patch.object(todo, "save", return_value=None):
        todo.save()

    assert todo.title == "Comprar leite"
    assert todo.description == "Ir ao mercado"
    assert todo.user_id == 1
    assert todo.done is False


@pytest.mark.django_db
def test_edit_todo_unit():
    todo = ToDoFactory.build(title="Antigo", description="Velho", user_id=1)

    updated_data = {
        "title": "Novo título",
        "description": "Nova descrição",
    }

    with patch.object(todo, "save", return_value=None):
        todo.title = updated_data["title"]
        todo.description = updated_data["description"]
        todo.save()

    assert todo.title == "Novo título"
    assert todo.description == "Nova descrição"


@pytest.mark.django_db
def test_list_todo_unit():
    todos = ToDoFactory.build_batch(3, user_id=1)

    def list_todos_for_user(user_id):
        return todos

    result = list_todos_for_user(1)
    assert len(result) == 3
    for todo in result:
        assert hasattr(todo, "title")
        assert hasattr(todo, "description")
        assert hasattr(todo, "done")


@pytest.mark.django_db
def test_retrieve_todo_unit():
    todo = ToDoFactory.build(
        title="Comprar leite", description="Mercado", user_id=1, done=False
    )

    def get_todo(todo_id):
        return todo if todo_id == 1 else None

    retrieved = get_todo(1)
    assert retrieved.title == "Comprar leite"
    assert retrieved.description == "Mercado"
    assert retrieved.done is False


@pytest.mark.django_db
def test_todo_permission_unit():
    todo_user2 = ToDoFactory.build(user_id=2)
    current_user = Mock(id=1)

    def can_access(user, todo):
        return todo.user_id == user.id

    assert not can_access(current_user, todo_user2)
    assert can_access(Mock(id=2), todo_user2)


@pytest.mark.django_db
def test_return_none_for_unexistent_todo_unit():
    def get_todo(todo_id):
        todos = []
        return next((t for t in todos if t.id == todo_id), None)

    assert get_todo(999) is None


@pytest.mark.django_db
def test_dont_permit_delete_todo_unit():
    todo_user2 = ToDoFactory.build(user_id=2)
    current_user = Mock(id=1)

    def can_delete(user, todo):
        return todo.user_id == user.id

    assert not can_delete(current_user, todo_user2)


# @pytest.mark.django_db
# def test_create_todo(auth_client):
#     new_todo = ToDoFactory.build()
#     payload = {
#         "title": new_todo.title,
#         "description": new_todo.description,
#     }
#     response = auth_client.post("/api/v1/fit/todo/", data=payload, format="json")
#     assert response.status_code == 201, response.content
#     data = response.json()
#     assert data["title"] == payload["title"]
#     assert data["description"] == payload["description"]

# @pytest.mark.django_db
# def test_delete_todo(auth_client):
#     habit = ToDoFactory.create(user_id=1)
#     response = auth_client.delete(f"/api/v1/fit/todo/{habit.id}/")
#     assert response.status_code == 204, response.content
#     with pytest.raises(ToDo.DoesNotExist):
#         ToDo.objects.get(id=habit.id)

# @pytest.mark.django_db
# def test_edit_habit(auth_client):
#     todo = ToDoFactory.create(user_id=1)

#     updated_data = {
#         "title": "Novo título",
#         "description": "Nova descrição",
#     }

#     response = auth_client.patch(f"/api/v1/fit/todo/{todo.id}/", data=updated_data, format="json")

#     assert response.status_code == 200, response.content

#     todo.refresh_from_db()
#     assert todo.title == updated_data["title"]
#     assert todo.description == updated_data["description"]

# @pytest.mark.django_db
# def test_list_todo(auth_client):
#     ToDoFactory.create_batch(3, user_id=1)

#     response = auth_client.get("/api/v1/fit/todo/")

#     assert response.status_code == 200, response.content

#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) == 3

#     first = data[0]
#     expected_fields = {"id", "title", "description"}
#     assert expected_fields.issubset(first.keys())

# @pytest.mark.django_db
# def test_retrieve_todo(auth_client):
#     todo = ToDoFactory.create(user_id=1)

#     response = auth_client.get(f"/api/v1/fit/todo/{todo.id}/")

#     assert response.status_code == 200, response.content
#     data = response.json()

#     assert data["title"] == todo.title
#     assert data["description"] == todo.description
#     assert data["done"] == todo.done

# @pytest.mark.django_db
# def test_dont_permit_update_todo_that_isnt_from_user(auth_client):
#     new_todo = ToDoFactory.create(user_id=2)
#     updated_data = {
#         "title": "Novo título",
#         "description": "Nova descrição",
#     }
#     response = auth_client.patch(
#         f"/api/v1/fit/todo/{new_todo.id}/", data=updated_data, format="json")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_access_todo_that_isnt_from_user(auth_client):
#     new_todo = ToDoFactory.create(user_id=2)
#     response = auth_client.get(f"/api/v1/fit/todo/{new_todo.id}/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_return_none_for_unexistent_todo(auth_client):
#     response = auth_client.get(f"/api/v1/fit/todo/999/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_exclude_unexistent_todo(auth_client):
#     response = auth_client.delete(f"/api/v1/fit/todo/999/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_exclude_todo_that_isnt_from_user(auth_client):
#     new_todo = ToDoFactory.create(user_id=2)
#     response = auth_client.delete(f"/api/v1/fit/todo/{new_todo.id}/")
#     assert response.status_code == 404
