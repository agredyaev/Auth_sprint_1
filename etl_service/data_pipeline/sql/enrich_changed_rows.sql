SELECT DISTINCT
    fw.id, fw.updated_at
FROM
    content.film_work fw
JOIN
    content.{table_name}_film_work tfw ON tfw.film_work_id = fw.id
WHERE
    tfw.{table_name}_id IN %s
ORDER BY
    fw.updated_at;