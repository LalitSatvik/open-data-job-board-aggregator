from app.auth.jwt import create_access_token, decode_access_token


def test_create_and_decode_round_trips_user_id():
    token = create_access_token(user_id=7)
    assert decode_access_token(token) == 7


def test_decode_rejects_garbage_token():
    assert decode_access_token("not-a-real-token") is None
