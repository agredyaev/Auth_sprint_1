SELECT
   g.id,
   g.name,
   g.description,
   g.updated_at
FROM content.genre g
WHERE g.updated_at > %(updated_at)s
ORDER BY g.updated_at
;