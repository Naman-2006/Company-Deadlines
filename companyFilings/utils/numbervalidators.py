import re

def parse_company_numbers(raw_text):
    """
    Splits raw input, keeps every token exactly as typed,
    zero-pads numbers shorter than 8 chars,
    and marks invalid codes.
    """

    tokens = re.split(r"[,\s]+", raw_text.strip())
    valid_numbers = []
    errors = []

    for original in tokens:
        if not original:
            continue

        cleaned = original.strip().upper()

        # If it's all digits, pad to 8 characters
        if cleaned.isdigit():
            padded = cleaned.zfill(8)
            valid_numbers.append(padded)
            continue

        # If it begins with letters, keep original (SC, OC, NI…)
        if re.match(r"^[A-Z]{2}[0-9]+$", cleaned):
            # If numeric part is shorter than 6 digits → pad right part
            prefix = cleaned[:2]
            digits = cleaned[2:]
            padded_digits = digits.zfill(6)
            valid_numbers.append(prefix + padded_digits)
            continue

        # Otherwise → mark as invalid
        errors.append(f"{original} – invalid code")

    return valid_numbers, errors
