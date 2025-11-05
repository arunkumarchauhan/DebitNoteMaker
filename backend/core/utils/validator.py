from typing import Annotated
from pydantic import AfterValidator
def validate_positive_int_string(v: str | None=None) -> str|None:
    if v is None:
        return v
    try:
        # Attempt to convert to an integer
        int_val = int(v.strip())
        # Check if it is a positive integer
        if int_val <= 0:
            raise ValueError("Value must be a positive integer (greater than 0)")
        return v.strip()
    except ValueError as e:
        # Re-raise as a ValueError that Pydantic can catch
        raise ValueError(f"Invalid input: {e}")
PositiveIntStringOrNone = Annotated[str| None, AfterValidator(validate_positive_int_string)]
