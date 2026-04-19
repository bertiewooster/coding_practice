import re
from dataclasses import dataclass

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

# payload = {
# "address": {
#     "street": "123 Main St",
#     "zip": "90210",
# },
# }

# schema = {
#     "name": {"type": "string", "required": True},
#     "address": {
#         "properties": {
#             "street": {"type": "string", "required": True},
#             "zip": {"type": "string", "pattern": r"^\d{5}$"},
#         }
#     },
# }

payload = {
    # "name": "Al",           # will test: required + min_length
    "name": "Al",
    "age": 150,  # will test: max
    "active": 1,  # will test: wrong type (int instead of bool)
    "address": {
        "street": "123 Main St",
        "zip": "9ABC1",  # will test: pattern
    },
    "lab": None,  # will test: not required, None nested object (skip silently)
    "sample": "not a dict",  # will test: expected an object
}

schema = {
    "name": {"type": "string", "required": True, "min_length": 3},
    "age": {"type": "integer", "min": 0, "max": 120},
    "active": {"type": "boolean"},
    "address": {
        "properties": {
            "street": {"type": "string", "required": True},
            "zip": {"type": "string", "pattern": r"^\d{5}$"},
        }
    },
    "lab": {
        "properties": {
            "name": {"type": "string", "required": True},
        }
    },
    "sample": {
        "properties": {
            "id": {"type": "string"},
        }
    },
    "missing_required": {"type": "string", "required": True},
}


descr_class = {"boolean": bool, "integer": int, "string": str}


@dataclass
class ValidationError:
    """Helper to format error messages"""

    path: list
    message: str

    def __str__(self):
        return f"{'.'.join(self.path)}: {self.message}"


def check_required(payload, field_name, rules, hierarchy):
    errors = []
    path = hierarchy + [field_name]
    is_required = rules.get("required", False)

    # If field is required by schema and
    #   there was no payload passed in (value is None) (guard against NoneType not iterable error)
    #   or field isn't included
    if is_required and ((payload is None) or (field_name not in payload)):
        error = ValidationError(path=path, message="required field missing.")
        errors.append(error)
    return errors


def check_nested(value, field_name, rules, hierarchy):
    errors = []
    path = hierarchy + [field_name]
    # Not required and not present; skip silently
    if value is None:
        return errors
    if not isinstance(value, dict):
        error = ValidationError(path=path, message="expected an object")
        errors.append(error)
        return errors
    errors_recursive = validate(
        payload=value,
        schema=rules["properties"],
        hierarchy=hierarchy + [field_name],
    )
    errors.extend(errors_recursive)
    return errors


def check_type(field_name, value, hierarchy, cls_should_be, has_type):
    errors = []
    path = hierarchy + [field_name]

    # Check field's (data) type
    if has_type:
        if type(value) is not cls_should_be:
            error = ValidationError(
                path=path,
                message=f"expected {cls_should_be.__name__}, got {type(value).__name__}",
            )
            errors.append(error)
    return errors


def check_integer(value, rules, hierarchy, field_name):
    errors = []
    path = hierarchy + [field_name]

    # Check min
    if "min" in rules:
        min_val = rules.get("min", None)
        if min_val is not None:
            if value < min_val:
                error = ValidationError(
                    path=path,
                    message=f"{value} is below minimum {min_val}",
                )
                errors.append(error)

    # Check max
    if "max" in rules:
        max_val = rules.get("max", None)
        if max_val is not None:
            if value > max_val:
                error = ValidationError(
                    path=path,
                    message=f"{value} is above maximum {max_val}",
                )
                errors.append(error)

    return errors


def check_string(value, rules, hierarchy, field_name):
    errors = []
    path = hierarchy + [field_name]
    # Check min_length
    if "min_length" in rules:
        min_length = rules.get("min_length", None)
        if min_length is not None:
            if len(value) < min_length:
                error = ValidationError(
                    path=path,
                    message=f"Min length {min_length} not met",
                )
                errors.append(error)

    # Check pattern
    if "pattern" in rules:
        pattern = rules.get("pattern", None)
        if pattern is not None:
            if not re.fullmatch(pattern=pattern, string=value):
                error = ValidationError(path=path, message=f"Pattern {pattern} not met")
                errors.append(error)
    return errors


type_checkers = {str: check_string, int: check_integer}


def validate(payload, schema, hierarchy=None):
    if hierarchy is None:
        hierarchy = []
    errors = []

    # Iterate through schema = field_name: rules
    for field_name, rules in schema.items():
        # Fetch this field from the payload
        value = payload.get(field_name) if payload else None

        # Check if field is required
        # Do this before checking is nested so that a required field won't crash
        # by calling None.get(field_name) aka value.get(field_name)
        required_error = check_required(
            payload=payload, field_name=field_name, rules=rules, hierarchy=hierarchy
        )
        if required_error:
            errors += required_error
            continue

        # Check if this is a nested field
        if "properties" in rules:
            errors += check_nested(value, field_name, rules, hierarchy)
            continue

        # Extract type info: will be used in multiple checkers below
        expected_type = rules.get("type", None)
        cls_should_be = descr_class.get(expected_type)
        has_type = "type" in rules

        # Check type
        type_error = check_type(field_name, value, hierarchy, cls_should_be, has_type)
        if type_error:
            errors += type_error
            continue

        # Type checkers
        if cls_should_be in type_checkers:
            errors += type_checkers[cls_should_be](value, rules, hierarchy, field_name)
    return errors


errors = validate(payload=payload, schema=schema)

# For display
for error in errors:
    print(error)

# For JSON API response
error: ValidationError
json_api_response = []
for error in errors:
    json_api_response += [{"path": error.path, "message": error.message}]
print(json_api_response)

# For filtering
address_errors = [error for error in errors if "address" in error.path]
for error in address_errors:
    print(error)
