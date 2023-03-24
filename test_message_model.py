"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        m1 = Message(text="Test Message 1", user_id=self.u1_id)
        m2 = Message(text="Test Message 2", user_id=self.u2_id)

        db.session.add_all([m1, m2])
        db.session.commit()

        self.m1_id = m1.id
        self.m2_id = m2.id

        l1 = Like(message_id=self.m2_id, user_id=self.u1_id)
        l2 = Like(message_id=self.m1_id, user_id=self.u2_id)

        db.session.add_all([l1, l2])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        with self.client as c:
            u1 = User.query.get(self.u1_id)
            m2 = Message.query.get(self.m1_id)

            self.assertTrue(len(u1.messages), 1)
            self.assertIn(m2, u1.messages)

            self.assertTrue(u1 == m2.user)

        # Test that user.message/message.user works,
        # Test that message is added to db

    # def test_create_message()
        # Test that a valid message is created

    # def test_create_message_invalid()
        # Test that message is not created if non-nullable fields are
        # None.

    # def test_liking_users()
        # Test relationship between message <-> users (liking_users)
        # Test relationship between message <-> likes (liked_messages)
