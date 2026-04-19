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
        },
        "active": {"type": "boolean"},
    }
    result = validate(payload=payload, schema=schema)
    assert result == []


def test_required():
    payload = {}
    schema = {
        "name": {
            "type": "string",
            "required": True,
        },
    }
    result = validate(payload=payload, schema=schema)
    assert "name: required field missing" in result


def test_boolean():
    payload = {"active": True}  # integer, not boolean
    schema = {"active": {"type": "integer"}}
    result = validate(payload=payload, schema=schema)
    assert "active: expected int, got bool" in result


def test_min():
    payload = {
        "age": -25,
    }

    schema = {
        "age": {
            "type": "integer",
            "min": 0,
        },
    }
    result = validate(payload=payload, schema=schema)
    assert "age: expected min 0, got -25" in result


def test_max():
    payload = {
        "age": 150,
    }

    schema = {
        "age": {
            "type": "integer",
            "max": 120,
        },
    }
    result = validate(payload=payload, schema=schema)
    assert "age: expected max 120, got 150" in result
