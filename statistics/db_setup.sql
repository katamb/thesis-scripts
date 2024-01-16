CREATE TABLE dataset(
    file_name VARCHAR(250) PRIMARY KEY,
    original_file_name VARCHAR(250),
    cwe_id VARCHAR(250),
    cwe_id VARCHAR(250),
    cwe_present BOOLEAN,
    cwe_description text
);


CREATE TABLE results(
    dataset_name VARCHAR(250),
    prompt_name VARCHAR(250) NOT NULL,
    file_name VARCHAR(250) NOT NULL,
    vulnerability_present BOOLEAN,
    identified_cwe_ids VARCHAR(250),
    time_taken NUMERIC(16, 8),
    tokens_used VARCHAR(250),
    cost NUMERIC(16, 8),
    created_at date,
    CONSTRAINT results_pkey PRIMARY KEY (prompt_name, file_name)
);
--DROP table results;