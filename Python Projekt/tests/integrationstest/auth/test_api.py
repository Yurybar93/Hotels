import pytest





@pytest.mark.parametrize(
    "first_name, last_name, email, password, status_code", [
        ("Testname", "Testlastname", "test@testmail.com", "12345678", 200),  
        ("Testname2", "Testlastname", "test2@testmail.com", "12345678", 200), 
        ("Testname", "Testlastname", "test3@testmail.com", "12345678", 200), 
        ("Testname", "Testlastname", "test@testmail.com", "12345678", 409),  
    ]
)
async def test_register_user(ac, first_name, last_name, email, password, status_code):
    response = await ac.post(
        "/auth/register",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"


@pytest.mark.parametrize(
     "email, password, status_code", [
        ("test@testmail.com", "12345678", 200),  
        ("test2@testmail.com", "12345678", 200), 
        ("test3@testmail.com", "12345678", 200), 
        ("test@testmail.com", "123456789", 401), 
        ("testfalse@testmail.com", "12345678", 404), 
    ] 
)
async def test_login_user(ac, email, password, status_code):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "access_token" in res
        assert isinstance(res["access_token"], str)
        assert len(res["access_token"]) > 0


@pytest.mark.parametrize(
    "first_name, last_name, email, password, status_code", [
        ("Testname", "Testlastname", "test@testmail.com", "12345678", 200),  
        ("Testname2", "Testlastname", "test2@testmail.com", "12345678", 200), 
        ("Testname", "Testlastname", "test3@testmail.com", "12345678", 200), 
    ]
)
async def test_get_me(ac, email, password, first_name, last_name, status_code):
     log_response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
     assert log_response.status_code == status_code
   
     me_response = await ac.get("/auth/me")
     if status_code == 200:
            assert me_response.status_code == 200
            res = me_response.json()
            assert isinstance(res, dict)
            assert res["email"] == email
            assert res["first_name"] == first_name
            assert res["last_name"] == last_name


@pytest.mark.parametrize(
     "email, password, status_code", [
        ("test@testmail.com", "12345678", 200),  
        ("test2@testmail.com", "12345678", 200), 
        ("test3@testmail.com", "12345678", 200), 
    ] 
)
async def test_logout_user(ac, email, password, status_code):
     log_response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
     log_response.status_code = status_code
     
     logout_response = await ac.post("/auth/logout")
     assert logout_response.status_code == 200
     res = logout_response.json()
     assert isinstance(res, dict)
     assert res["status"] == "OK"
     assert ac.cookies.get("access_token") is None

            



    
