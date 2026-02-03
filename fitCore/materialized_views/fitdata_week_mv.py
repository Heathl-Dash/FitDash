from .base import MaterializedView


class FitDataWeek(MaterializedView):
    view_name = "fitdata_week"
    sql = """
    DROP MATERIALIZED VIEW IF EXISTS fitdata_week;
    CREATE MATERIALIZED VIEW fitdata_week AS
    SELECT *
    FROM "fitCore_fitdata"
    WHERE fit_date >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '1 week')
      AND fit_date <  DATE_TRUNC('week', CURRENT_DATE);
    """
    frequency = "weekly"
