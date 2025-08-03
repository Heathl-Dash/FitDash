DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_matviews WHERE matviewname = 'habit_semana') THEN
    CREATE MATERIALIZED VIEW habit_semana AS
    WITH semana AS (
        SELECT date_trunc('week', now() - interval '1 week') AS inicio,
               date_trunc('week', now()) AS fim
    )
    SELECT
        user_id,
        date(created) AS dia,
        COUNT(*) AS total_habits,
        COUNT(*) FILTER (WHERE positive) AS habits_positivos,
        COUNT(*) FILTER (WHERE negative) AS habits_negativos
    FROM "fitCore_habit", semana
    WHERE created >= semana.inicio AND created < semana.fim
    GROUP BY user_id, date(created);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_matviews WHERE matviewname = 'todo_semana') THEN
    CREATE MATERIALIZED VIEW todo_semana AS
    WITH semana AS (
        SELECT date_trunc('week', now() - interval '1 week') AS inicio,
               date_trunc('week', now()) AS fim
    )
    SELECT
        user_id,
        date(created) AS dia,
        COUNT(*) AS total_todos,
        COUNT(*) FILTER (WHERE done) AS todos_concluidos
    FROM "fitCore_todo", semana
    WHERE created >= semana.inicio AND created < semana.fim
    GROUP BY user_id, date(created);
  END IF;
END$$;