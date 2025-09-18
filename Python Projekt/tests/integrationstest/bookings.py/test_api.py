async def test_add_booking(autheticated_ac, db):
    room_id = (await db.rooms.get_all())[0].id
    response = await autheticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-07-01",
            "date_to": "2024-07-10"
        }
    )

    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "OK"
    assert "data" in res