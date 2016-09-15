# -*- coding: utf-8 -*-

import flask
import flask_restful
import sqlalchemy
import sqlalchemy.orm

from mfit_service import models
from mfit_service import resources
from mfit_service import services
from mfit_service import views


class WorkoutsPrograms(resources.Base):

    def get(self, workout_id, workout_program_id):
        try:
            workout_program = (
                self._db_context.query(models.WorkoutsMovements)
                                .filter_by(workout_movement_id=workout_program_id)
                                .one())
        except sqlalchemy.orm.exc.NoResultFound:
            return flask_restful.abort(404)
        else:
            return WorkoutsPrograms.to_json(workout_program=workout_program)

    def patch(self, workout_id, workout_program_id):
        workout_program = (
            self._db_context.query(models.WorkoutsMovements)
                            .filter_by(workout_movement_id=workout_program_id)
                            .one())

        for attribute, value in flask.request.get_json().items():
            setattr(workout_program, attribute, value)

        # TODO (duyn): ME-192
        self._db_context.add(workout_program, updated_by=999)
        self._db_context.commit()

        body = WorkoutsPrograms.to_json(workout_program=workout_program)

        self._db_context.close()

        return body

    def delete(self, workout_id, workout_program_id):
        self._db_context.query(models.WorkoutsMovements) \
                        .filter_by(workout_movement_id=workout_program_id) \
                        .delete(synchronize_session=False)
        self._db_context.commit()
        self._db_context.close()

    @staticmethod
    def get_self_link(workout_program):
        self_link = services.api.url_for(
            WorkoutsPrograms,
            workout_id=workout_program.workout_id,
            workout_program_id=workout_program.workout_movement_id,
            _external=True)
        return self_link

    @staticmethod
    def to_json(workout_program):
        links = {
            'self': WorkoutsPrograms.get_self_link(workout_program=workout_program)
        }

        body = views.WorkoutsPrograms().dump(workout_program).data
        body.update({'links': links})

        return body

