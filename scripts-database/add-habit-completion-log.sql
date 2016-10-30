CREATE OR REPLACE FUNCTION pg_temp.addHabitCompletionLog (
	usersEmailAddress varchar(64),
	habitsName varchar(32)
)
RETURNS void AS
$$
BEGIN
	INSERT INTO attempts_logs (
		attempts_id,
		habits_id,
		sets_remaining,
		created_by
	)
	(
		WITH last_logs_today AS (
			SELECT
				MAX(attempts_logs.created_on) AS created_on,
				attempts_logs.habits_id
			FROM attempts_logs
			INNER JOIN attempts ON attempts.id = attempts_logs.attempts_id
			INNER JOIN users ON users.id = attempts.users_id
			INNER JOIN habits ON habits.id = attempts_logs.habits_id
			WHERE
				attempts.starts_at <= CURRENT_TIMESTAMP AND
				attempts.ends_at > CURRENT_TIMESTAMP AND
				users.email_address = usersEmailAddress AND
				habits.name = habitsName AND
				attempts_logs.created_on >= CURRENT_DATE
			GROUP BY attempts_logs.habits_id
		)
		SELECT
			attempts_logs.attempts_id,
			attempts_logs.habits_id,
			attempts_logs.sets_remaining - 1 AS sets_remaining,
			attempts.users_id AS created_by
		FROM attempts_logs
		INNER JOIN last_logs_today ON
			last_logs_today.created_on = attempts_logs.created_on AND
			last_logs_today.habits_id = attempts_logs.habits_id
		INNER JOIN attempts ON attempts.id = attempts_logs.attempts_id
		INNER JOIN users ON users.id = attempts.users_id
		WHERE
			attempts.starts_at <= CURRENT_TIMESTAMP AND
			attempts.ends_at > CURRENT_TIMESTAMP AND
			users.email_address = usersEmailAddress
	);
END
$$
LANGUAGE plpgsql;