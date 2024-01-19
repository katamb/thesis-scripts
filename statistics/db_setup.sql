CREATE TABLE dataset(
    dataset_name VARCHAR(250),
    file_name VARCHAR(250),
    original_file_name VARCHAR(250),
    cwe_id VARCHAR(250),
    cwe_present BOOLEAN,
    acceptable_cwe_ids text,
    cwe_description text,
    CONSTRAINT dataset_pkey PRIMARY KEY (dataset_name, file_name)
);

COMMENT ON TABLE dataset IS 'Table to store information about datasets and associated files';
COMMENT ON COLUMN dataset.dataset_name IS 'Value for uniquely identifying datasets';
COMMENT ON COLUMN dataset.file_name IS 'Value for uniquely identifying files within datasets';
COMMENT ON COLUMN dataset.original_file_name IS 'Original file name before any modifications';
COMMENT ON COLUMN dataset.cwe_id IS 'CWE (Common Weakness Enumeration) ID associated with the dataset';
COMMENT ON COLUMN dataset.cwe_present IS 'Indicates whether CWE is present in the file';
COMMENT ON COLUMN dataset.acceptable_cwe_ids IS 'Space-separated list of acceptable CWE IDs';
COMMENT ON COLUMN dataset.cwe_description IS 'Text field to store the description of CWE';
COMMENT ON CONSTRAINT dataset_pkey ON dataset IS 'Ensure the combination of dataset_name and file_name is unique';


CREATE TABLE results(
    dataset_name VARCHAR(250) NOT NULL,
    llm_model VARCHAR(250),
    prompt_name VARCHAR(250) NOT NULL,
    file_name VARCHAR(250) NOT NULL,
    vulnerability_detected BOOLEAN,
    identified_cwe_ids VARCHAR(250),
    time_taken NUMERIC(16, 8),
    tokens_used VARCHAR(250),
    cost NUMERIC(16, 8),
    created_at date,
    CONSTRAINT results_pkey PRIMARY KEY (prompt_name, file_name),
    FOREIGN KEY (dataset_name, file_name) REFERENCES dataset (dataset_name, file_name)
);

COMMENT ON TABLE results IS 'Table to store results of vulnerability analysis on datasets';
COMMENT ON COLUMN results.dataset_name IS 'Name of the dataset associated with the result entry';
COMMENT ON COLUMN results.llm_model IS 'Name of the language model used for analysis (if applicable)';
COMMENT ON COLUMN results.prompt_name IS 'Name of the prompt used for the analysis (not nullable)';
COMMENT ON COLUMN results.file_name IS 'Name of the file associated with the result entry (not nullable)';
COMMENT ON COLUMN results.vulnerability_detected IS 'Indicates whether vulnerabilities were identified in the analysis';
COMMENT ON COLUMN results.identified_cwe_ids IS 'Space-separated list of identified CWE (Common Weakness Enumeration) IDs';
COMMENT ON COLUMN results.time_taken IS 'Time taken for the analysis in seconds (numeric with precision 16, scale 8)';
COMMENT ON COLUMN results.tokens_used IS 'Tokens used for the analysis (if applicable)';
COMMENT ON COLUMN results.cost IS 'Cost associated with the analysis (numeric with precision 16, scale 8)';
COMMENT ON COLUMN results.created_at IS 'Date when the result entry was created';
COMMENT ON CONSTRAINT results_pkey ON results IS 'Primary key constraint for unique combinations of prompt_name and file_name';
