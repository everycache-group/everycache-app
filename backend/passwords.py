from passlib.hash import pbkdf2_sha256 as sha256


def generate_hash(s: str) -> str:
    return sha256.hash(s)


def verify_password(password: str, hash_: str) -> bool:
    return sha256.verify(password, hash_)
