-- Get true positives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS TRUE
    AND res.vulnerability_detected IS TRUE;

-- Get true negatives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS FALSE
    AND res.vulnerability_detected IS FALSE;

-- Get false positives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS FALSE
    AND res.vulnerability_detected IS TRUE;

-- Get false negatives
SELECT ds.file_name, ds.cwe_id, ds.cwe_present, res.identified_cwe_ids, res.vulnerability_detected, res.time_taken, res.cost
FROM results res
INNER JOIN public.dataset ds ON res.file_name = ds.file_name
    AND res.dataset_name = ds.dataset_name
WHERE res.prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND ds.dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND res.llm_model = '<model_name>'  -- e.g. gpt-4-1106-preview
    AND ds.cwe_present IS TRUE
    AND res.vulnerability_detected IS FALSE;

-- Get overall data
SELECT avg(cost) as avg_cost, sum(cost) as sum_cost, avg(time_taken) as avg_time_taken, sum(time_taken) as sum_time_taken
FROM results
WHERE prompt_name = '<prompt_name>'  -- e.g. dataflow_analysis_prompt
    AND dataset_name = '<ds_name>'  -- e.g. juliet-top-25-subset-34
    AND llm_model = '<model_name>';  -- e.g. gpt-4-1106-preview

-- Overall data v2
select cwe_id, count(*)
from dataset
group by cwe_id;