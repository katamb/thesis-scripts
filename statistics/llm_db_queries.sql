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
            WHEN NOT ds.cwe_present AND
                 (NOT res.vulnerability_detected OR
                    (res.vulnerability_detected AND NOT EXISTS (
                        SELECT 1
                        FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                        JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
                    ))
                 )
            THEN TRUE
            ELSE FALSE
        END AS true_negative,
        CASE
            WHEN ds.cwe_present AND
                 (NOT res.vulnerability_detected OR
                    (res.vulnerability_detected AND NOT EXISTS (
                        SELECT 1
                        FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                        JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
                    ))
                 )
            THEN TRUE
            ELSE FALSE
        END AS false_negative,
        CASE
            WHEN NOT ds.cwe_present AND res.vulnerability_detected AND EXISTS (
                SELECT 1
                FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
            ) THEN TRUE
            ELSE FALSE
        END AS false_positive,
        CASE
            WHEN ds.cwe_present AND res.vulnerability_detected AND EXISTS (
                SELECT 1
                FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
            ) THEN TRUE
            ELSE FALSE
        END AS true_positive
    FROM dataset ds
    LEFT JOIN llm_results res ON res.file_name = ds.file_name
        AND res.dataset_name = ds.dataset_name
        AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
        AND res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    WHERE ds.dataset_name = '<dataset>'  -- e.g. juliet-top-25-subset-34
) sq
-- GROUP BY cwe_id  -- Uncomment for grouped response
;

-- Get true positives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM llm_results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS TRUE
    AND res.vulnerability_detected IS TRUE;

-- Get true negatives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM llm_results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS FALSE
    AND res.vulnerability_detected IS FALSE;

-- Get false positives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM llm_results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS FALSE
    AND res.vulnerability_detected IS TRUE;

-- Get false negatives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM llm_results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS TRUE
    AND res.vulnerability_detected IS FALSE;

-- Get overall data
SELECT avg(cost) as avg_cost, sum(cost) as sum_cost, avg(time_taken) as avg_time_taken, sum(time_taken) as sum_time_taken
FROM llm_results
WHERE prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND llm_model = '<model_name>';  -- e.g. gpt-4-1106-preview

-- Overall data v2
select cwe_id, count(*)
from dataset
group by cwe_id;