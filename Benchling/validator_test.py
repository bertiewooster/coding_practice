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
    assert "age: -25 is below minimum 0" in result


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
    assert "age: 150 is above maximum 120" in result


def test_min_length():
    payload = {
        "name": "Sample A",
    }

    schema = {
        "name": {
            "type": "string",
            "min_length": 20,
        },
    }
    result = validate(payload=payload, schema=schema)
    assert "name: Min length 20 not met" in result


def test_pattern():
    payload = {
        "zip": "z2345",
    }

    schema = {
        "zip": {"type": "string", "pattern": r"^\d{5}$"},
    }
    result = validate(payload=payload, schema=schema)
    assert "zip: Pattern ^\\d{5}$ not met" in result
