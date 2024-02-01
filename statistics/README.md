# Result analysis

In this folder are the scripts required for analysing the results. 
We utilize a relational database to analyse the results. To start off, run `docker compose up` in this folder.

## Static code analysis tool (SCAT) results
The static code analysis results are held in the `scat_results` table. There is a file called `scat_db_queries.sql`
with the query that was used to get the results.
Previously, we used a specific marker "CWE-NR" for CWE's detected by static analysis tools, which seemed to be correctly
identified problems, but which were not related to the security vulnerabilities we are looking at. 

