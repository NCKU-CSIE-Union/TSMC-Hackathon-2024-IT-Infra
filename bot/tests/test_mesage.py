from bot.message import send_embedded_message


def test_send_embedded_message():
    message_dict = {
        "title": "This is a test message",
        "description": "This is a test message",
        "color": 0x00FF00,
        "fields": [
            {
                "name": "Field 1",
                "value": "This is a field",
                "inline": False,
            },
            {
                "name": "Field 2",
                "value": "This is a field",
                "inline": False,
            },
        ],
    }
    send_embedded_message(message_dict)
    assert True
