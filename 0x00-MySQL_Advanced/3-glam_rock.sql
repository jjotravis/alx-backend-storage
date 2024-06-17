-- Lists all bands with glam rock
-- ranked by longetivity
SELECT
    band_name,
    CASE
        WHEN split IS NULL THEN (2022 - formed)
    ELSE (split - formed)
    END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'