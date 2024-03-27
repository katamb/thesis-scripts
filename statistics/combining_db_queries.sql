WITH scat_res AS (
    SELECT file_name, dataset_name, scat_tool, STRING_AGG(identified_cwe_ids, ' ') AS concatenated_cwe_ids
    FROM scat_results
    GROUP BY file_name, dataset_name, scat_tool
), cql_pos_res AS (
    SELECT file_name
    FROM (
        SELECT
            ds.file_name
        FROM dataset ds
        LEFT JOIN scat_res res ON res.file_name = ds.file_name
            AND res.dataset_name = ds.dataset_name
            AND res.scat_tool = 'codeql-extended-quality'
        WHERE ds.dataset_name = 'juliet-top-25-subset-34'
            AND ds.cwe_present  -- uncomment for only TP results
            AND EXISTS (
                    SELECT 1
                    FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                    JOIN unnest(string_to_array(res.concatenated_cwe_ids, ' ')) AS id2 ON id1 = id2
                )
    ) sq
), sb_pos_res AS (
    SELECT file_name
    FROM (
        SELECT
            ds.file_name
        FROM dataset ds
        LEFT JOIN scat_res res ON res.file_name = ds.file_name
            AND res.dataset_name = ds.dataset_name
            AND res.scat_tool = 'spotbugs-extended'
        WHERE ds.dataset_name = 'juliet-top-25-subset-34'
            AND ds.cwe_present  -- uncomment for only TP results
            AND EXISTS (
                    SELECT 1
                    FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                    JOIN unnest(string_to_array(res.concatenated_cwe_ids, ' ')) AS id2 ON id1 = id2
                )
    ) sq
), llm_pos_res AS (
    SELECT file_name
    FROM (
        SELECT
            ds.file_name
        FROM dataset ds
        LEFT JOIN llm_results res ON res.file_name = ds.file_name
            AND res.dataset_name = ds.dataset_name
            AND res.llm_model = 'gpt-4-0125-preview'  -- e.g. gpt-4-1106-preview
            AND res.prompt_name = 'dataflow_analysis_prompt_rci_improve'  -- e.g. dataflow_analysis_prompt
        WHERE ds.dataset_name = 'juliet-top-25-subset-34'  -- e.g. juliet-top-25-subset-34
            AND ds.cwe_present  -- uncomment for only TP results
            AND res.vulnerability_detected
            AND EXISTS (
                    SELECT 1
                    FROM unnest(string_to_array(ds.acceptable_cwe_ids, ' ')) AS id1
                    JOIN unnest(string_to_array(res.identified_cwe_ids, ' ')) AS id2 ON id1 = id2
                )
        ) sq
)
SELECT file_name
from cql_pos_res
    union
SELECT file_name
from sb_pos_res
    union
SELECT file_name
from llm_pos_res
;