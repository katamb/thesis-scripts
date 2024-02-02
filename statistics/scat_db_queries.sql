--- SCAT ---

-- Single query --
SELECT
    -- cwe_id,  -- Uncomment for grouped response
    COUNT(DISTINCT CASE WHEN sq.true_positive THEN sq.file_name END) as true_positive_count,
    COUNT(DISTINCT CASE WHEN sq.false_positive THEN sq.file_name END) as false_positive_count,
    COUNT(DISTINCT CASE WHEN sq.true_negative THEN sq.file_name END) as true_negative_count,
    COUNT(DISTINCT CASE WHEN sq.false_negative THEN sq.file_name END) as false_negative_count
FROM (
    SELECT
        ds.file_name,
        ds.cwe_present,
        -- ds.cwe_id,  -- Uncomment for grouped response
        CASE
            WHEN NOT ds.cwe_present AND NOT EXISTS (
                SELECT 1
                FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                INNER JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
            ) THEN TRUE
            ELSE FALSE
        END AS true_negative,
        CASE
            WHEN ds.cwe_present AND NOT EXISTS (
                SELECT 1
                FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                INNER JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
            ) THEN TRUE
            ELSE FALSE
        END AS false_negative,
        CASE
            WHEN NOT ds.cwe_present AND EXISTS (
                SELECT 1
                FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
            ) THEN TRUE
            ELSE FALSE
        END AS false_positive,
        CASE
            WHEN ds.cwe_present AND EXISTS (
                SELECT 1
                FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
            ) THEN TRUE
            ELSE FALSE
        END AS true_positive
    FROM dataset ds
    LEFT JOIN scat_results res ON res.file_name = ds.file_name
        AND res.dataset_name = ds.dataset_name
        AND res.scat_tool = '<tool>'  -- e.g. codeql
    WHERE ds.dataset_name = '<dataset>'  -- e.g. juliet-top-25-subset-34
) sq
-- GROUP BY cwe_id  -- Uncomment for grouped response
;


-- Query one-by-one --
-- true negative
SELECT count(distinct sq.file_name) as true_negative_count
FROM (
    SELECT ds.file_name
    FROM dataset ds
    LEFT JOIN scat_results res ON res.file_name = ds.file_name
                                      AND res.dataset_name = ds.dataset_name
                                      AND res.scat_tool = 'spotbugs'
    WHERE NOT ds.cwe_present
        AND ds.dataset_name = 'juliet-top-25-subset-34'
        AND NOT exists(
            SELECT 1
            FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                INNER JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
        )
) sq
;

-- false negative
SELECT count(distinct sq.file_name) as false_negative_count
FROM (
    SELECT ds.file_name
    FROM dataset ds
    LEFT JOIN scat_results res ON res.file_name = ds.file_name
                                      AND res.dataset_name = ds.dataset_name
                                      AND res.scat_tool = 'spotbugs'
    WHERE ds.cwe_present
        AND ds.dataset_name = 'juliet-top-25-subset-34'
        AND NOT exists(
            SELECT 1
            FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                INNER JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
        )
) sq
;

-- false positive
SELECT count(distinct sq.file_name) as false_positive_count
FROM (
    SELECT ds.file_name
    FROM dataset ds
    LEFT JOIN scat_results res ON res.file_name = ds.file_name
                                      AND res.dataset_name = ds.dataset_name
                                      AND res.scat_tool = 'spotbugs'
    WHERE NOT ds.cwe_present
    AND ds.dataset_name = 'juliet-top-25-subset-34'
    AND exists(
        SELECT 1
        FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
        JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
    )
) sq
;

-- true positive
SELECT count(distinct sq.file_name) as true_positive_count
FROM (
    SELECT ds.file_name
    FROM dataset ds
    LEFT JOIN scat_results res ON res.file_name = ds.file_name
                                      AND res.dataset_name = ds.dataset_name
                                      AND res.scat_tool = 'spotbugs'
    WHERE ds.cwe_present
    AND ds.dataset_name = 'juliet-top-25-subset-34'
    AND exists (
        SELECT 1
        FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
        JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
    )
) sq
;
