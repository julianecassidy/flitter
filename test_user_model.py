"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///flitter_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages, no followers & no liked messages
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.liked_messages), 0)

    #NOTE: Do we need to have self.client as c???
    def test_is_following(self):
        with self.client as c:
            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)
            u1.following.append(u2)
            db.session.commit()

            self.assertTrue(u1.is_following(u2))

    def test_is_not_following(self):
        with self.client as c:
            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)

            self.assertFalse(u1.is_following(u2))

    def test_is_followed_by(self):
        with self.client as c:
            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)
            u1.followers.append(u2)
            db.session.commit()

            self.assertTrue(u1.is_followed_by(u2))

    def test_is_not_followed_by(self):
        with self.client as c:
            u1 = User.query.get(self.u1_id)
            u2 = User.query.get(self.u2_id)

            self.assertFalse(u1.is_followed_by(u2))

    def test_user_signup(self):
        with self.client as c:
            password = 'password'
            new_user = User.signup(
                username="TestUser",
                email="abc@email.com",
                password=password
            )

            self.assertIsInstance(new_user, User)
            # password is hashed
            self.assertNotEqual(new_user.password, password)

            #NOTE: test this here or in route?
            # num_of_users = User.query.all()
            # self.assertEqual(len(num_of_users, 3))

    def test_user_signup_fail(self):
        with self.client as c:

            password = 'password'

            # Tests no username
            User.signup(
                username=None,
                email="abc@email.com",
                password=password
            )

            with self.assertRaises(exc.IntegrityError):
                db.session.flush()

            db.session.rollback()

            # Tests no email
            User.signup(
                username="TestUser",
                email=None,
                password=password
            )

            with self.assertRaises(exc.IntegrityError):
                db.session.flush()

            db.session.rollback()

            # Tests duplicate username
            User.signup(
                username="u1",
                email="abc@email.com",
                password=password
            )

            with self.assertRaises(exc.IntegrityError):
                db.session.flush()

            db.session.rollback()

            #Tests duplicate email
            User.signup(
                username="TestUser3",
                email="u2@email.com",
                password=password
            )

            with self.assertRaises(exc.IntegrityError):
                db.session.flush()

            db.session.rollback()


    def test_user_authenticate_valid(self):
        with self.client as c:

            u1 = User.query.get(self.u1_id)

            logged_in = User.authenticate(username="u1", password="password")

            self.assertIsInstance(logged_in, User)


    def test_user_authenticate_invalid(self):
        with self.client as c:

            # Tests failed attempt with invalid username
            invalid_username_attempt = User.authenticate(
                username="wrong_name",
                password="password")

            self.assertFalse(invalid_username_attempt)

            # Tests failed attempt with invalid password
            invalid_password_attempt = User.authenticate(
                username="u1",
                password="wrong_password"
            )

            self.assertFalse(invalid_password_attempt)
