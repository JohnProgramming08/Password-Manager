from api.database import Insert, Select, VerifyUser
import pytest
from services import Encryption


# Insert
# Inserting a new user into the database
def test_insert_user_valid(app):
    with app.app_context():
        assert Insert.insert_user("sigma", "male") is True


def test_insert_user_invalid(app):
    with app.app_context():
        Insert.insert_user("sigma", "male")
        assert Insert.insert_user("sigma", "anything") is False


# Select
# Checking if an email exists in the database
@pytest.mark.parametrize("email_hash", ["sigma", "Dylan", "top"])
def test_email_exists_valid(many_users_app, email_hash):
    with many_users_app.app_context():
        assert Select.email_exists(email_hash) is True


def test_email_exists_invalid(many_users_app):
    with many_users_app.app_context():
        assert Select.email_exists("invalid") is False


# Checking if the users details are correct
@pytest.mark.parametrize(
    "email_hash, password",
    [("sigma", "male"), ("Dylan", "Scully"), ("top", "grades")],
)
def test_are_details_correct_valid(many_users_app, email_hash, password):
    with many_users_app.app_context():
        assert Select.are_details_correct(email_hash, password) is True


def test_are_details_correct_invalid(many_users_app):
    with many_users_app.app_context():
        assert Select.are_details_correct("invalid", "wrong") is False


# VerifyUser
# Verifying the users details
@pytest.mark.parametrize(
    "email_hash, password",
    [
        ("sigma", "male"),
        ("Dylan", "Scully"),
        ("top", "grades"),
        ("new", "guy"),
    ],
)
def test_verify_valid(many_users_app, email_hash, password):
    with many_users_app.app_context():
        assert VerifyUser.verify(email_hash, password) is True


def test_verify_invalid(many_users_app):
    with many_users_app.app_context():
        assert VerifyUser.verify("sigma", "nope") is False
