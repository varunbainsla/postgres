SELECT aws_s3.table_import_from_s3('public."AutoDebitSchedule"', 'identifier,"Item"', '(format csv, header true)',
'nira-postgres-migration-data',
'data_generation/AutoDebitSchedule/AutoDebitSchedule-data11.csv',
'ap-south-1',
'aws-access-key', 'aws-secret-key'
)


-- ALTER TABLE public."AutoDebitSchedule"
-- ALTER COLUMN identifier TYPE character varying;