import re

# payload = {
#     "name": "Sample A",
#     # "name": 27,
#     "age": 150,
#     # "age": "25",
#     "active": True,
#     "zip": "z2345",
# }

# schema = {
#     "name": {
#         "type": "string",
#         "required": True,
#         "min_length": 20,
#     },
#     "age": {
#         "type": "integer",
#         # "required": True,
#         "min": 0,
#         "max": 120,
#     },
#     "active": {"type": "boolean"},
#     "zip": {"type": "string", "pattern": r"^\d{5}$"},
# }

# payload = {"active": 1}  # integer, not boolean
# schema = {"active": {"type": "boolean"}}

# payload = {"active": True}  # integer, not boolean
# schema = {"active": {"type": "integer"}}

payload = {
    "address": {
        "street": "123 Main St",
        "zip": "90210",
    },
}

schema = {
    "address": {
        "properties": {
            "street": {"type": "string", "required": True},
            "zip": {"type": "string", "pattern": r"^\d{5}$"},
        }
    },
}

descr_class = {"boolean": bool, "integer": int, "string": str}


def format_error(hierarchy, field_name, message):
    full_hierarchy = hierarchy + [field_name]
    full_message = f"{'.'.join(full_hierarchy)}: {message}"
    return full_message


def validate(payload, schema, hierarchy=None):
    if hierarchy is None:
        hierarchy = []
    errors = []

    # Iterate through schema = field_name: rules
    for field_name, rules in schema.items():
        # print(f"{field_name=} {rules=}")

        # Check if field is required
        # Do this before checking is nested so that a required field won't crash
        # by calling None.get(field_name) aka value.get(field_name)
        is_required = rules.get("required", False)
        if is_required and ((payload is None) or (field_name not in payload)):
            errors.append(
                format_error(
                    hierarchy=hierarchy,
                    field_name=field_name,
                    message="required field missing.",
                )
            )
            continue

        # Fetch this field from the payload
        value = payload.get(field_name)

        # Check if is nested
        if "properties" in rules:
            # Not required and not present; skip silently
            if value is None:
                continue
            if not isinstance(value, dict):
                errors.append(
                    format_error(
                        hierarchy=hierarchy,
                        field_name=field_name,
                        message="expected an object",
                    )
                )
                continue
            errors_recursive = validate(
                payload=value,
                schema=schema[field_name]["properties"],
                hierarchy=hierarchy + [field_name],
            )
            errors.extend(errors_recursive)
            continue

        expected_type = rules.get("type", None)
        cls_should_be = descr_class.get(expected_type)
        has_type = "type" in rules

        # Check field's (data) type
        if has_type:
            if type(value) is not cls_should_be:
                errors.append(
                    format_error(
                        hierarchy=hierarchy,
                        field_name=field_name,
                        message=f"expected {cls_should_be.__name__}, got {type(value).__name__}",
                    )
                )
                continue

        # Check min
        if "min" in rules:
            min_val = rules.get("min", None)
            if min_val is not None:
                if value < min_val:
                    errors.append(
                        format_error(
                            hierarchy=hierarchy,
                            field_name=field_name,
                            message=f"{value} is below minimum {min_val}",
                        )
                    )

        # Check max
        if "max" in rules:
            max_val = rules.get("max", None)
            if max_val is not None:
                if value > max_val:
                    errors.append(
                        format_error(
                            hierarchy=hierarchy,
                            field_name=field_name,
                            message=f"{value} is above maximum {max_val}",
                        )
                    )

        # Check for strings
        if has_type and cls_should_be is str:
            # Check min_length
            if "min_length" in rules:
                min_length = rules.get("min_length", None)
                if min_length is not None:
                    if len(value) < min_length:
                        errors.append(
                            format_error(
                                hierarchy=hierarchy,
                                field_name=field_name,
                                message=f"Min length {min_length} not met",
                            )
                        )

            # Check pattern
            if "pattern" in rules:
                pattern = rules.get("pattern", None)
                if pattern is not None:
                    if not re.fullmatch(pattern=pattern, string=value):
                        errors.append(
                            format_error(
                                hierarchy=hierarchy,
                                field_name=field_name,
                                message=f"Pattern {pattern} not met",
                            )
                        )
                        pass

    return errors


v = validate(payload=payload, schema=schema)
print(v)
