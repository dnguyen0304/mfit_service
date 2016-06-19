DROP TABLE IF EXISTS users_workouts;

CREATE TABLE users_workouts (
	user_workout_id		serial						PRIMARY KEY,
	user_id				int							REFERENCES users (user_id),
	workout_id			int							REFERENCES workouts (workout_id),
	created_on			timestamp	NOT NULL		DEFAULT CURRENT_TIMESTAMP,
	created_by			int			NOT NULL,
	updated_on			timestamp,
	updated_by			int
);
