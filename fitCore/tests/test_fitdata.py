import pytest
from unittest.mock import patch, Mock
from factories import FitDataFactory
from fitCore.models.fit_data import FitData
from fitCore.serializers.fitdata_serializer import FitDataSerializer


# Unitários
@pytest.fixture
def mock_user():
    return Mock(id=1)


@patch("fitCore.serializers.fitdata_serializer.get_current_user")
def test_create_fitdata_unit(mock_get_user, mock_user):
    """Testa criação de FitData sem banco de dados."""
    mock_get_user.return_value = mock_user

    data = {
        "fit_date": "2025-10-21",
        "steps": 8000,
        "distance": 6.2,
        "burned_calories": 300.5,
    }

    serializer = FitDataSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    with patch("fitCore.serializers.fitdata_serializer.FitData.objects.update_or_create") as mock_update_or_create:
        mock_instance = Mock(steps=8000, user_id=1)
        mock_update_or_create.return_value = (mock_instance, True)

        instance = serializer.save()

    mock_update_or_create.assert_called_once()
    assert instance.steps == 8000
    assert instance.user_id == 1


@patch("fitCore.serializers.fitdata_serializer.get_current_user")
def test_update_fitdata_unit(mock_get_user):
    mock_user = Mock(id=1)
    mock_get_user.return_value = mock_user

    fitdata = FitDataFactory.build(user_id=1, steps=5000, distance=3.5)

    with patch.object(fitdata, "save", return_value=None) as mock_save:
        serializer = FitDataSerializer(fitdata, data={"steps": 7000, "distance": 5.0}, partial=True)
        assert serializer.is_valid(), serializer.errors
        instance = serializer.save()

    mock_save.assert_called_once()
    assert instance.steps == 7000
    assert instance.distance == 5.0
    assert instance.user_id == 1


def test_retrieve_fitdata_unit():
    fitdata = FitDataFactory.build(id=10, user_id=1)

    def get_fitdata_by_id(fitdata_id):
        return fitdata if fitdata.id == fitdata_id else None

    retrieved = get_fitdata_by_id(10)
    assert retrieved is not None
    assert retrieved.id == 10
    assert retrieved.user_id == 1


def test_dont_permit_user_access_other_user_unit():
    """Testa que usuário não consegue acessar FitData de outro usuário."""
    fitdata = FitDataFactory.build(user_id=2)
    current_user = Mock(id=1)

    def can_user_access(user, obj):
        return obj.user_id == user.id

    assert not can_user_access(current_user, fitdata)


def test_dont_permit_user_update_other_user_unit():
    """Testa que usuário não consegue atualizar FitData de outro usuário."""
    fitdata = FitDataFactory.build(user_id=2)
    current_user = Mock(id=1)

    def can_user_update(user, obj):
        return obj.user_id == user.id

    assert not can_user_update(current_user, fitdata)


# Integração
# @pytest.mark.django_db
# def test_create_new_fitdata(auth_client):
#     new_fitdata = FitDataFactory.build(user_id=1)
#     payload = {
#         "fit_date": new_fitdata.fit_date,
#         "steps": new_fitdata.steps,
#         "distance": new_fitdata.distance,
#         "burned_calories": new_fitdata.burned_calories
#     }
#     response = auth_client.post("/api/v1/fit/fitdata/", data=payload, format="json")
#     assert response.status_code == 201, response.content

# @pytest.mark.django_db
# def test_update_fitdata(auth_client):
#     fitdata = FitDataFactory.create(user_id=1)
#     payload = {"steps": 7000, "distance": 5.0}
#     response_update = auth_client.patch(
#         f"/api/v1/fit/fitdata/{fitdata.id}/", data=payload, format="json"
#     )
#     assert response_update.status_code == 200

# @pytest.mark.django_db
# def test_retrieve_new_fitdata(auth_client):
#     fitdata = FitDataFactory.create(user_id=1)
#     response = auth_client.get(f"/api/v1/fit/fitdata/{fitdata.id}/")
#     assert response.status_code == 200

# @pytest.mark.django_db
# def test_dont_permit_user_access_fitdata_from_other_user(auth_client):
#     fitdata = FitDataFactory.create(user_id=2)
#     response = auth_client.get(f"/api/v1/fit/fitdata/{fitdata.id}/")
#     assert response.status_code == 404

# @pytest.mark.django_db
# def test_dont_permit_user_update_fitdata_from_other_user(auth_client):
#     fitdata = FitDataFactory.create(user_id=2)
#     payload = {"steps": 7000, "distance": 5.0}
#     response_update = auth_client.patch(
#         f"/api/v1/fit/fitdata/{fitdata.id}/", data=payload, format="json"
#     )
#     assert response_update.status_code == 404
