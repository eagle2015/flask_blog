# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import wtforms
from wtforms.validators import DataRequired
from wtforms import validators



from models import Entry, Tag, User

class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            # display tags a comma-separated list
            return ', '.join(tag.name for tag in self.data)
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        #filter out any empty tag names
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        # determine which tag is new
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        # create list of unsaved tag instance for new tag
        new_tags = [Tag(name=name) for name in new_names]
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class EntryForm(wtforms.Form):
    title = wtforms.StringField('Title', validators=[DataRequired()])
    body = wtforms.TextAreaField('Body', validators=[DataRequired()])
    status = wtforms.SelectField(
        'Entry status',
        choices=(
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')
        ), coerce=int
    )
    tags = TagField(
        'Tags',
        description='Separate multiple tags with commas.'
    )

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry

class ImageForm(wtforms.Form):
    file = wtforms.FileField('Image file')

class LoginForm(wtforms.Form):
    email = wtforms.StringField("Email", validators=[validators.DataRequired()])
    password = wtforms.PasswordField("Password", validators=[validators.DataRequired()])
    remember_me = wtforms.BooleanField("Remember me?", default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password.")
            return False
        return True








