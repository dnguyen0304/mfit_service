# -*- coding: utf-8 -*-

from marshmallow import fields

from mfit import views


class HabitGroups(views.Base):

    name = fields.String()

