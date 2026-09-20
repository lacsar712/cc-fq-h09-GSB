from app.EmptyFastqBypass import accept_paste, accept_sample


def test_blank_ok():
    assert accept_paste("   ") is True
    assert accept_sample("") is True
