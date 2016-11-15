# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from mfit import models


class Habits(models.Base):

    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column()

    habit_groups = relationship('HabitGroups', back_populates='habit')

    def __init__(self, name):

        """
        Habits model.

        Parameters
        ----------
        name : str
            Name.

        Attributes
        ----------
        id : int
            Unique identifier.
        name : str
            Name.
        habit_groups : mfit.models.Routines
            Routines model.
        created_at : datetime.datetime
            When the entity was originally created.
        created_by : int
            Who originally created the entity.
        updated_at : datetime.datetime
            When the entity was last updated.
        updated_by : int
            Who last updated the entity.
        """

        self.name = name

    def __repr__(self):
        repr_ = '{}(name="{}")'
        return repr_.format(self.__class__.__name__, self.name)

