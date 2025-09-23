import pytest


from tests.conftest import null_pull_db


@pytest.mark.parametrize(
    "date_from, date_to, room_id, status_code",
    [
        ("2024-07-01", "2024-07-10", 1, 200),
        ("2024-07-01", "2024-07-10", 1, 200),
        ("2024-07-01", "2024-07-10", 1, 200),
        ("2024-07-01", "2024-07-10", 1, 200),
        ("2024-07-01", "2024-07-10", 1, 200),
        ("2024-07-01", "2024-07-10", 1, 409),
    ],
)
async def test_add_booking(autheticated_ac, db, date_from, date_to, room_id, status_code):
    response = await autheticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_bookings():
    async for _db in null_pull_db():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "date_from, date_to, room_id, number_bookings",
    [
        ("2024-07-01", "2024-07-10", 1, 1),
        ("2024-07-01", "2024-07-10", 1, 2),
        ("2024-07-01", "2024-07-10", 1, 3),
    ],
)
async def test_add_and_get_bookings(
    date_from,
    date_to,
    room_id,
    number_bookings,
    delete_bookings,
    autheticated_ac,
):
    booking_resp = await autheticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert booking_resp.status_code == 200

    me_resp = await autheticated_ac.get("/bookings/me")
    assert me_resp.status_code == 200
    assert len(me_resp.json()) == number_bookings
