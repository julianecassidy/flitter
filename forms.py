from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, URLField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )

    image_url = StringField(
        '(Optional) Image URL',
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[Length(min=6)],
    )

class EditUserForm(FlaskForm):
    """Form to update user's information."""
    #TODO: Add length restrictions
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    bio = TextAreaField(
        'Bio',
        validators=[Optional()]
    )

    #TODO: Add URL() and URLField() before deploying
    image_url = StringField(
        'Profile Image',
        validators=[Optional()]
    )

    header_image_url = StringField(
        'Header Image',
        validators=[Optional()]
    )

    password = PasswordField(
        'Enter Password',
        validators=[DataRequired()]
    )


class CSRFForm(FlaskForm):
    """Empty form to add CSRF protection."""
