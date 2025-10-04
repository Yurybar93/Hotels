async def test_get_hotel(ac):
    response = await ac.get("/hotels", params={"date_from": "2025-09-30", "date_to": "2025-10-01"})

    assert response.status_code == 200
