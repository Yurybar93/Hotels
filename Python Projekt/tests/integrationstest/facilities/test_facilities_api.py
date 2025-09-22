async def test_get_facilites(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200


async def test_create_facility(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Test Facility",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["data"]["title"] == "Test Facility"
