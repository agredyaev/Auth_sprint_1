SELECT DISTINCT
    fw.id, fw.updated_at
FROM
    content.film_work fw
JOIN
    content.{table_name} tfw ON tfw.film_work_id = fw.id
WHERE
    tfw.{column_name} IN %s
ORDER BY
    fw.updated_at;