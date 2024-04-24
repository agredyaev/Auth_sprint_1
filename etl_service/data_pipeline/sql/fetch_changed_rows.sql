SELECT
    id, updated_at
FROM
    content.{table_name}
WHERE
    updated_at > %s
ORDER BY
    updated_at;