"""
This file contains some helper decorators for checking
that the request body is valid JSON and contains all the
fields that the function requires as arguments.
"""


from functools import wraps
from json import loads
from result import Ok, Error, to_error
import inspect

# Create nice error messages
InvalidJSON = to_error("Invalid JSON", "The request body was not valid JSON")


def MissingField(field): return to_error(
    "Missing field", f"The request body was missing the field {field}")
# ---


def fields(request):
    """
    Decorator that checks that the request body is valid JSON,
    contains all the fields that the function requires as arguments
    and passes them to the function as arguments.

    Usage:
    ```python
    @require.fields(request)
    def my_function(arg1, arg2):
        # Do stuff
    ```
    This will check that the request body is valid JSON and contains
    the fields `arg1` and `arg2`. If it does, it will pass them to the
    function as arguments.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = request.json
            except:
                try:
                    data = loads(request.data)
                except:
                    return Error((InvalidJSON, 400))
            # Get string representation of args
            fields = inspect.getfullargspec(func).args
            args = []
            for field in fields:
                if field not in data.keys():
                    return Error((MissingField(field), 400))
                else:
                    args.append(data[field])
            return func(*args, **kwargs)
        return wrapper
    return decorator
