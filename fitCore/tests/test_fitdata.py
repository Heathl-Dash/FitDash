import pytest
from unittest.mock import patch
from factories import FitDataFactory

@pytest.mark.django_db
def test_create_new_fitdata(auth_client):
    new_fitdata = FitDataFactory.build(user_id=1)
    payload = {
        "fit_date": new_fitdata.fit_date,
        "steps": new_fitdata.steps,
        "distance": new_fitdata.distance,
        "burned_calories": new_fitdata.burned_calories
    }
    response = auth_client.post("/api/v1/fit/fitdata/", data=payload, format="json")
    assert response.status_code == 201, response.content

@pytest.mark.django_db
def test_update_fitdata(auth_client):
    fitdata = FitDataFactory.create(user_id=1)
    payload = {"steps": 7000, "distance": 5.0}
    response_update = auth_client.patch(
        f"/api/v1/fit/fitdata/{fitdata.id}/", data=payload, format="json"
    )
    assert response_update.status_code == 200

@pytest.mark.django_db
def test_retrieve_new_fitdata(auth_client):
    fitdata = FitDataFactory.create(user_id=1)
    response = auth_client.get(f"/api/v1/fit/fitdata/{fitdata.id}/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_dont_permit_user_access_fitdata_from_other_user(auth_client):
    fitdata = FitDataFactory.create(user_id=2)
    response = auth_client.get(f"/api/v1/fit/fitdata/{fitdata.id}/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_dont_permit_user_update_fitdata_from_other_user(auth_client):
    fitdata = FitDataFactory.create(user_id=2)
    payload = {"steps": 7000, "distance": 5.0}
    response_update = auth_client.patch(
        f"/api/v1/fit/fitdata/{fitdata.id}/", data=payload, format="json"
    )
    assert response_update.status_code == 404