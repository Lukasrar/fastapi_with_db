from .utils import *
from routers.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get('/user/get-user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "username": "lukas",
        "email": "lukas@example.com",
        "first_name": "Lukas",
        "last_name": "Example",
        "is_active": True,
        "role": "admin",
        "phone_number": "1234567890",
    }

def test_change_password_success(test_user):
    response = client.put("/user/change-password", json={"current_password": "test", "new_password": "test123"})
    assert response.status_code == status.HTTP_204_NO_CONTENT



def test_change_password_invalid_password(test_user):
    response = client.put("/user/change-password", json={"current_password": "test2", "new_password": "test123"})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

def test_change_phone_number_success(test_user):
    response = client.put("/user/change-phone-number/2222")
    assert response.status_code == status.HTTP_204_NO_CONTENT

