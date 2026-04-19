from validator import validate


def test_original():
    payload = {
        "name": "Sample A",
        "age": 25,
        "active": True,
    }
    schema = {
        "name": {
            "type": "string",
            "required": True,
        },
        "age": {
            "type": "integer",
            # "required": True,
        },
        "active": {"type": "boolean"},
    }
    result = validate(payload=payload, schema=schema)
    assert result == []


def test_required():
    payload = {
        "age": 25,
        "active": True,
    }
    schema = {
        "name": {
            "type": "string",
            "required": True,
        },
        "age": {
            "type": "integer",
            # "required": True,
        },
        "active": {"type": "boolean"},
    }
    result = validate(payload=payload, schema=schema)
    assert "name: required field missing" in result


def test_boolean():
    payload = {"active": True}  # integer, not boolean
    schema = {"active": {"type": "integer"}}
    result = validate(payload=payload, schema=schema)
    assert "active: expected int, got bool" in result
