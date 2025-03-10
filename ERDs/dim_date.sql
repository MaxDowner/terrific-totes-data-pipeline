SELECT 
    day AS date_id,
    EXTRACT(YEAR FROM day) AS year,
    EXTRACT(MONTH FROM day) AS month,
    EXTRACT(DAY FROM day) as day,
    EXTRACT(ISODOW FROM day) AS day_of_week,
    TO_CHAR(day, 'Day') AS day_name,
    TO_CHAR(day, 'Month') as month_name,
    EXTRACT(QUARTER FROM day) AS quarter
FROM generate_series('2022-01-01'::date, '2030-12-31'::date, '1 day') AS day;

