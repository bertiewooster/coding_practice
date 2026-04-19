payload = {
    "name": "Sample A",
    # "name": 27,
    "age": 150,
    # "age": "25",
    "active": True,
}

schema = {
    "name": {
        "type": "string",
        "required": True,
        "min_length": 20,
    },
    "age": {
        "type": "integer",
        # "required": True,
        "min": 0,
        "max": 120,
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
        if is_required and field_name not in payload:
            errors.append(f"{field_name}: required field missing")
            continue

        expected_type = rules.get("type", None)
        cls_should_be = descr_class.get(expected_type)
        has_type = "type" in rules

        # Check field's (data) type
        if has_type:
            # cls_should_be = descr_class[expected_type]
            if type(value) is not cls_should_be:
                errors.append(
                    f"{field_name}: expected {cls_should_be.__name__}, got {type(value).__name__}"
                )
                continue

        # Check min
        if "min" in rules:
            min_val = rules.get("min", None)
            if min_val is not None:
                if value < min_val:
                    errors.append(f"{field_name}: {value} is below minimum {min_val}")

        # Check max
        if "max" in rules:
            max_val = rules.get("max", None)
            if max_val is not None:
                if value > max_val:
                    errors.append(f"{field_name}: {value} is above maximum {max_val}")

        # Check for strings
        if has_type and cls_should_be.__name__ == "str":
            if "min_length" in rules:
                min_length = rules.get("min_length", None)
                if len(value) < min_length:
                    errors.append(f"{field_name}: Min length {min_length} not met")

    return errors


v = validate(payload=payload, schema=schema)
print(v)
