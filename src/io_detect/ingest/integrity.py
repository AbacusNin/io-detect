import hashlib

class IntegrityError(ValueError):
    pass

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify(path: str, expected: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise IntegrityError(f"checksum mismatch: {actual} != {expected}")
