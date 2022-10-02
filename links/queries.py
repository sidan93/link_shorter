SQL_INSERT_SHORT_LINK = '''
    WITH RECURSIVE
    generate_uuid AS (
        SELECT
            gen_random_uuid() as key,
            1 as length
    ),
    prepare_links AS (
        SELECT
            key,
            length,
            substr(key::TEXT, 0, length + 1) || substr(key::TEXT, 34, length) as short_url
        FROM generate_uuid

        UNION ALL

        SELECT
            key,
            length + 1,
            substr(key::TEXT, 0, length + 2) || substr(key::TEXT, 34, length + 1) as short_url
        FROM prepare_links
        WHERE EXISTS(
                SELECT 1
                FROM link
                WHERE prepare_links.short_url = link.short_url
            )
    ),
    pre_data AS (
        SELECT
            key as id,
            (:long_url)::TEXT as long_url,
            short_url as short_url,
            False AS deleted,
            now() AS created_at
        FROM prepare_links
        ORDER BY octet_length(short_url) DESC
        LIMIT 1
    )
    INSERT INTO link (id, long_url, short_url, deleted, created_at)
    SELECT *
    FROM pre_data
    RETURNING id, long_url, short_url
'''

SQL_INSERT_INTO_HISTORY = '''
    INSERT INTO history (link, created_at)
    VALUES((:link), now())
'''

SQL_GET_VISITS_FOR_LAST_DAY = '''
    WITH current_link AS (
        SELECT id as link
        FROM link
        WHERE 
            short_url = (:short_url)
            AND deleted IS FALSE
    )
    SELECT 
        link as link, 
        COUNT(1) as count
    FROM history
    NATURAL JOIN current_link
    GROUP BY link
'''
