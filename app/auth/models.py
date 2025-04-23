from app.auth.utils import hash_password

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": hash_password("adminpass"),
    }
}
