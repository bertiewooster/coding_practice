payload = {
    # "name": "Sample A",
    # "name": 27,
    # "age": 25,
    # "age": "25",
    # "active": True,
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

# payload = {"active": 1}  # integer, not boolean
# schema = {"active": {"type": "boolean"}}

# payload = {"active": True}  # integer, not boolean
# schema = {"active": {"type": "integer"}}

descr_class = {"boolean": bool, "integer": int, "string": str}


def validate(payload, schema):
    errors = []

    # Iterate through schema = field_name: rules
    for field_name, rules in schema.items():
        # Fetch this field from the payload
        value = payload.get(field_name)
        print(f"{field_name=} {rules=}")

        # Check if field is required
        is_required = rules.get("required", False)
        if is_required:
            try:
                payload[field_name]
            except KeyError:
                errors.append(f"{field_name}: required field missing")
                continue

        # Check field's (data) type
        expected_type = rules.get("type", None)

        if expected_type in descr_class:
            cls_should_be = descr_class[expected_type]
            if type(value) is not cls_should_be:
                errors.append(
                    f"{field_name}: expected {cls_should_be.__name__}, got {type(value).__name__}"
                )

    return errors


v = validate(payload=payload, schema=schema)
print(v)
