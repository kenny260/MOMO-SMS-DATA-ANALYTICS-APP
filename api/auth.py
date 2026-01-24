import base64

# Hardcoded credentials for now (can be replaced with DB later)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

def check_auth(headers):
    """
    Checks Authorization header for Basic Auth.
    Returns True if valid, False otherwise.
    """

    auth_header = headers.get("Authorization")

    if not auth_header:
        return False

    if not auth_header.startswith("Basic "):
        return False

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode("utf-8")

        username, password = decoded_str.split(":")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return True
        return False

    except Exception:
        return False
