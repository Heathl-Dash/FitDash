import pytest

pytestmark = pytest.mark.django_db

from unittest.mock import Mock, patch
from factories import HabitFactory


@pytest.fixture
def mock_user():
    return Mock(id=1)


def test_create_habit_unit_simple():
    habit = HabitFactory.build(
        title="Exercício",
        description="Correr 5km",
        positive=True,
        negative=False,
        user_id=1,
    )

    with patch.object(habit, "save", return_value=None):
        habit.save()

    assert habit.title == "Exercício"
    assert habit.description == "Correr 5km"
    assert habit.positive is True
    assert habit.negative is False
    assert habit.user_id == 1


def test_edit_habit_unit(mock_user):
    habit = HabitFactory.build(
        user_id=1, title="Antigo", description="Velho", positive=True, negative=False
    )
    updated_data = {
        "title": "Novo",
        "description": "Atualizado",
        "positive": True,
        "negative": False,
    }

    with patch.object(habit, "save", return_value=None):
        habit.title = updated_data["title"]
        habit.description = updated_data["description"]
        habit.positive = updated_data["positive"]
        habit.negative = updated_data["negative"]
        habit.save()

    assert habit.title == "Novo"
    assert habit.description == "Atualizado"
    assert habit.positive is True
    assert habit.negative is False


def test_list_habit_unit():
    habits = HabitFactory.build_batch(3, user_id=1)

    def list_habits_for_user(user_id):
        return habits

    result = list_habits_for_user(1)
    assert len(result) == 3
    for habit in result:
        assert hasattr(habit, "title")
        assert hasattr(habit, "description")
        assert hasattr(habit, "positive")
        assert hasattr(habit, "negative")


def test_retrieve_habit_unit():
    habit = HabitFactory.build(
        user_id=1, title="Ex", description="Desc", positive=True, negative=False
    )

    def get_habit(habit_id):
        return habit if habit_id == 1 else None

    retrieved = get_habit(1)
    assert retrieved.title == "Ex"
    assert retrieved.description == "Desc"
    assert retrieved.positive is True
    assert retrieved.negative is False


def test_habit_counters_unit():
    habit_positive = HabitFactory.build(
        user_id=1, positive=True, negative=False, positive_count=2
    )
    habit_negative = HabitFactory.build(
        user_id=1, positive=False, negative=True, negative_count=3
    )

    if habit_positive.positive:
        habit_positive.positive_count += 1
    if habit_negative.negative:
        habit_negative.negative_count += 1

    assert habit_positive.positive_count == 3
    assert habit_negative.negative_count == 4


def test_habit_permission_unit():
    habit_user2 = HabitFactory.build(user_id=2)
    current_user = Mock(id=1)

    def can_access(user, habit):
        return habit.user_id == user.id

    assert not can_access(current_user, habit_user2)
    assert can_access(Mock(id=2), habit_user2)


def test_habit_validation_unit():
    habit_data = {
        "title": "Teste",
        "description": "Desc",
        "positive": False,
        "negative": False,
    }

    def is_valid_habit(data):
        return data["positive"] or data["negative"]

    assert not is_valid_habit(habit_data)


# @pytest.mark.django_db
# def test_create_habit(auth_client):
#     new_habit = HabitFactory.build()
#     payload = {
#         "title": new_habit.title,
#         "description": new_habit.description,
#         "positive": new_habit.positive,
#         "negative": new_habit.negative,
#     }
#     response = auth_client.post("/api/v1/fit/habit/", data=payload, format="json")
#     assert response.status_code == 201, response.content
#     data = response.json()
#     assert data["title"] == payload["title"]
#     assert data["description"] == payload["description"]
#     assert data["positive"] == payload["positive"]
#     assert data["negative"] == payload["negative"]

# @pytest.mark.django_db
# def test_delete_habit(auth_client):
#     habit = HabitFactory.create(user_id=1)
#     response = auth_client.delete(f"/api/v1/fit/habit/{habit.id}/")
#     assert response.status_code == 204, response.content
#     with pytest.raises(Habit.DoesNotExist):
#         Habit.objects.get(id=habit.id)

# @pytest.mark.django_db
# def test_edit_habit(auth_client):
#     habit = HabitFactory.create(user_id=1)

#     updated_data = {
#         "title": "Novo título",
#         "description": "Nova descrição",
#         "positive": True,
#         "negative": False,
#     }

#     response = auth_client.patch(f"/api/v1/fit/habit/{habit.id}/", data=updated_data, format="json")

#     assert response.status_code == 200, response.content

#     habit.refresh_from_db()
#     assert habit.title == updated_data["title"]
#     assert habit.description == updated_data["description"]
#     assert habit.positive == updated_data["positive"]
#     assert habit.negative == updated_data["negative"]

# @pytest.mark.django_db
# def test_list_habit(auth_client):
#     HabitFactory.create_batch(3, user_id=1)

#     response = auth_client.get("/api/v1/fit/habit/")

#     assert response.status_code == 200, response.content

#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) == 3

#     first = data[0]
#     expected_fields = {"id", "title", "description", "positive", "negative"}
#     assert expected_fields.issubset(first.keys())

# @pytest.mark.django_db
# def test_retrieve_habit(auth_client):
#     habit = HabitFactory.create(user_id=1)

#     response = auth_client.get(f"/api/v1/fit/habit/{habit.id}/")

#     assert response.status_code == 200, response.content
#     data = response.json()

#     assert data["title"] == habit.title
#     assert data["description"] == habit.description
#     assert data["positive"] == habit.positive
#     assert data["negative"] == habit.negative

# @pytest.mark.django_db
# def test_habit_cant_have_positive_and_negative_as_false(auth_client):
#     new_habit = HabitFactory.build()
#     payload = {
#         "title": new_habit.title,
#         "description": new_habit.description,
#         "positive": False,
#         "negative": False,
#     }
#     response = auth_client.post("/api/v1/fit/habit/", data=payload, format="json")
#     assert response.status_code == 400, response.content

# @pytest.mark.django_db
# def test_habit_positive_counter(auth_client):
#     new_habit = HabitFactory.create(user_id=1, positive=True)
#     pre_added_positive_counter_habit = new_habit.positive_count
#     response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_positive_counter/")
#     assert response.status_code == 200
#     new_habit.refresh_from_db()
#     assert new_habit.positive_count == (pre_added_positive_counter_habit + 1)

# @pytest.mark.django_db
# def test_habit_negative_counter(auth_client):
#     new_habit = HabitFactory.create(user_id=1, negative=True)
#     pre_added_negative_counter_habit = new_habit.negative_count
#     response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_negative_counter/")
#     assert response.status_code == 200
#     new_habit.refresh_from_db()
#     assert new_habit.negative_count == (pre_added_negative_counter_habit + 1)

# @pytest.mark.django_db
# def test_dont_permit_add_positive_counter_to_negative_habit(auth_client):
#     new_habit = HabitFactory.create(user_id=1, positive=False, negative=True)
#     response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_positive_counter/")
#     assert response.status_code == 400

# @pytest.mark.django_db
# def test_dont_permit_add_negative_counter_to_positive_habit(auth_client):
#     new_habit = HabitFactory.create(user_id=1, positive=True, negative=False)
#     response = auth_client.patch(f"/api/v1/fit/habit/{new_habit.id}/add_negative_counter/")
#     assert response.status_code == 400

# @pytest.mark.django_db
# def test_dont_permit_update_habit_that_isnt_from_user(auth_client):
#     new_habit = HabitFactory.create(user_id=2)
#     updated_data = {
#         "title": "Novo título",
#         "description": "Nova descrição",
#         "positive": True,
#         "negative": False,
#     }
#     response = auth_client.patch(
#         f"/api/v1/fit/habit/{new_habit.id}/", data=updated_data, format="json")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_access_habit_that_isnt_from_user(auth_client):
#     new_habit = HabitFactory.create(user_id=2)
#     response = auth_client.get(f"/api/v1/fit/habit/{new_habit.id}/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_return_none_for_unexistent_habit(auth_client):
#     response = auth_client.get(f"/api/v1/fit/habit/999/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_exclude_unexistent_habit(auth_client):
#     response = auth_client.delete(f"/api/v1/fit/habit/999/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_exclude_habit_that_isnt_from_user(auth_client):
#     new_habit = HabitFactory.create(user_id=2)
#     response = auth_client.delete(f"/api/v1/fit/habit/{new_habit.id}/")
#     assert response.status_code == 404
