SELECT
    fw.id,
    fw.rating as rating,
    fw.title,
    fw.description,
    fw.updated_at,
    COALESCE(
        json_agg(DISTINCT g.name),'[]') as genres,
    COALESCE(
       json_agg(
           DISTINCT p.full_name
       ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
       '[]'
    ) as directors_names,
    COALESCE(
       json_agg(
           DISTINCT p.full_name
       ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
       '[]'
    ) as actors_names,
    COALESCE(
       json_agg(
            DISTINCT p.full_name
       ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
       '[]'
    ) as writers_names,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
        '[]'
    ) as directors,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
        '[]'
    ) as actors,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', p.id,
                'name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
        '[]'
    ) as writers
FROM
    content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE
    fw.updated_at > %(updated_at)s
    OR g.updated_at > %(updated_at)s
    OR p.updated_at > %(updated_at)s
GROUP BY
    fw.id
ORDER BY
    fw.updated_at DESC
 ;