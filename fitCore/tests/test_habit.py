import pytest
from factories import HabitFactory
from fitCore.models import Habit

@pytest.mark.django_db
def test_create_habit(auth_client):
    new_habit = HabitFactory.build()
    payload = {
        "title": new_habit.title,
        "description": new_habit.description,
        "positive": new_habit.positive,
        "negative": new_habit.negative,
    }
    response = auth_client.post("/api/v1/fit/habit/", data=payload, format="json")
    assert response.status_code == 201, response.content
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["positive"] == payload["positive"]
    assert data["negative"] == payload["negative"]

@pytest.mark.django_db
def test_delete_habit(auth_client):
    habit = HabitFactory.create(user_id=1)
    response = auth_client.delete(f"/api/v1/fit/habit/{habit.id}/")
    assert response.status_code == 204, response.content
    with pytest.raises(Habit.DoesNotExist):
        Habit.objects.get(id=habit.id)

@pytest.mark.django_db
def test_edit_habit(auth_client):
    habit = HabitFactory.create(user_id=1)

    updated_data = {
        "title": "Novo título",
        "description": "Nova descrição",
        "positive": True,
        "negative": False,
    }

    response = auth_client.patch(f"/api/v1/fit/habit/{habit.id}/", data=updated_data, format="json")
    
    assert response.status_code == 200, response.content

    habit.refresh_from_db()
    assert habit.title == updated_data["title"]
    assert habit.description == updated_data["description"]
    assert habit.positive == updated_data["positive"]
    assert habit.negative == updated_data["negative"]

@pytest.mark.django_db
def test_list_habit(auth_client):
    HabitFactory.create_batch(3, user_id=1)  

    response = auth_client.get("/api/v1/fit/habit/")

    assert response.status_code == 200, response.content

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    first = data[0]
    expected_fields = {"id", "title", "description", "positive", "negative"}
    assert expected_fields.issubset(first.keys())

@pytest.mark.django_db
def test_retrieve_habit(auth_client):
    habit = HabitFactory.create(user_id=1)

    response = auth_client.get(f"/api/v1/fit/habit/{habit.id}/")

    assert response.status_code == 200, response.content
    data = response.json()

    assert data["title"] == habit.title
    assert data["description"] == habit.description
    assert data["positive"] == habit.positive
    assert data["negative"] == habit.negative

@pytest.mark.django_db
def test_habit_cant_have_positive_and_negative_as_false(auth_client):
    new_habit = HabitFactory.build()
    payload = {
        "title": new_habit.title,
        "description": new_habit.description,
        "positive": False,
        "negative": False,
    }
    response = auth_client.post("/api/v1/fit/habit/", data=payload, format="json")
    assert response.status_code == 400, response.content

@pytest.mark.django_db
def test_habit_positive_counter(auth_client):
    new_habit = HabitFactory.create(user_id=1, positive=True)
    pre_added_positive_counter_habit = new_habit.positive_count
    response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_positive_counter/")
    assert response.status_code == 200
    new_habit.refresh_from_db()
    assert new_habit.positive_count == (pre_added_positive_counter_habit + 1)

@pytest.mark.django_db
def test_habit_negative_counter(auth_client):
    new_habit = HabitFactory.create(user_id=1, negative=True)
    pre_added_negative_counter_habit = new_habit.negative_count
    response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_negative_counter/")
    assert response.status_code == 200
    new_habit.refresh_from_db()
    assert new_habit.negative_count == (pre_added_negative_counter_habit + 1)

@pytest.mark.django_db
def test_dont_permit_add_positive_counter_to_negative_habit(auth_client):
    new_habit = HabitFactory.create(user_id=1, positive=False, negative=True)
    response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_positive_counter/")
    assert response.status_code == 400

@pytest.mark.django_db
def test_dont_permit_add_negative_counter_to_positive_habit(auth_client):
    new_habit = HabitFactory.create(user_id=1, positive=True, negative=False)
    response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_negative_counter/")
    assert response.status_code == 400

@pytest.mark.django_db
def test_dont_permit_update_habit_that_isnt_from_user(auth_client):
    new_habit = HabitFactory.create(user_id=2)
    updated_data = {
        "title": "Novo título",
        "description": "Nova descrição",
        "positive": True,
        "negative": False,
    }
    response = auth_client.patch(
        f"/api/v1/fit/habit/{new_habit.id}/", data=updated_data, format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_dont_permit_access_habit_that_isnt_from_user(auth_client):
    new_habit = HabitFactory.create(user_id=2)
    response = auth_client.get(f"/api/v1/fit/habit/{new_habit.id}/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_return_none_for_unexistent_habit(auth_client):
    response = auth_client.get(f"/api/v1/fit/habit/999/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_dont_permit_exclude_unexistent_habit(auth_client):
    response = auth_client.delete(f"/api/v1/fit/habit/999/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_dont_permit_exclude_habit_that_isnt_from_user(auth_client):
    new_habit = HabitFactory.create(user_id=2)
    response = auth_client.delete(f"/api/v1/fit/habit/{new_habit.id}/")
    assert response.status_code == 404
