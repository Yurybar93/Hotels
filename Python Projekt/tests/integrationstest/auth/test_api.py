import pytest


@pytest.mark.parametrize(
    "first_name, last_name, email, password, status_code",
    [
        ("Testname", "Testlastname", "test@testmail.com", "12345678", 200),
        ("Testname2", "Testlastname2", "test2@testmail.com", "12345678", 200),
        ("Testname3", "Testlastname3", "test3@testmail.com", "12345678", 200),
        ("Testname", "Testlastname", "test@testmail.com", "12345678", 409),
        ("Testname", "Testlastname", "test@testmail", "12345678", 422),
    ],
)
async def test_register_user(ac, first_name, last_name, email, password, status_code):
    response = await ac.post(
        "/auth/register",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"


@pytest.mark.parametrize(
    "first_name, last_name, email, password, status_code",
    [
        ("Testname", "Testlastname", "test@testmail.com", "12345678", 200),
        ("Testname2", "Testlastname2", "test2@testmail.com", "12345678", 200),
        ("Testname3", "Testlastname3", "test3@testmail.com", "12345678", 200),
        ("Testname", "Testlastname", "test@testmail.com", "123456789", 401),
        ("Testname", "Testlastname", "testfalse@testmail.com", "12345678", 404),
    ],
)
async def test_login_me_logout_user(ac, first_name, last_name, email, password, status_code):
    log_response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert log_response.status_code == status_code
    if status_code != 200:
        return
    res = log_response.json()
    assert isinstance(res, dict)
    assert "access_token" in res
    assert isinstance(res["access_token"], str)
    assert len(res["access_token"]) > 0

    me_response = await ac.get("/auth/me")
    if status_code != 200:
        return
    assert me_response.status_code == 200
    res = me_response.json()
    assert isinstance(res, dict)
    assert res["email"] == email
    assert res["first_name"] == first_name
    assert res["last_name"] == last_name

    logout_response = await ac.post("/auth/logout")
    if status_code != 200:
        return
    res = logout_response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert ac.cookies.get("access_token") is None
