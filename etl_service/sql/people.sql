WITH film_work_roles as (
    SELECT
        fw.id,
        fw.title,
        array_agg(pfw.role) as roles,
        pfw.person_id
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw on fw.id = pfw.film_work_id
        GROUP BY fw.id, pfw.person_id
)
SELECT
    p.id,
    p.full_name,
    p.updated_at,
    COALESCE(
        json_agg(
            DISTINCT jsonb_build_object(
                'id', fwr.id,
                'title', fwr.title,
                'roles', fwr.roles
            )
        ), '[]'
    ) as movies
FROM content.person p
LEFT JOIN film_work_roles fwr on fwr.person_id = p.id
WHERE p.updated_at > %(updated_at)s
GROUP BY p.id
ORDER BY p.updated_at
;