#!/bin/bash


# Set AWS credentials (replace with your own)
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""

# Set other variables
bucket_name="nira-postgres-migration-data"
prefix="data_generation/AutoDebitSchedule/"

# List files in S3 bucket and iterate over them
aws s3 ls "s3://$bucket_name/$prefix" | while read -r line; do
    file_name=$(echo "$line" | awk '{print $NF}')
    echo "Processing file: $file_name"

    # Run psql command for each file
    #psql -h nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com -p 5432 -U postgres -d nira-test-db -c "SELECT aws_s3.table_import_from_s3('public.\"AutoDebitSchedule\"', 'identifier,"Item"', '(format csv, header true)','nira-postgres-migration-data','$prefix$file_name','ap-south-1','aws-access-key', 'aws-secret-key')"

#psql -h nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com -p 5432 -U postgres -d nira-test-db -c "SELECT aws_s3.table_import_from_s3('public.\"AutoDebitSchedule\"', 'identifier,\"Item\"', '(format csv, header true)','nira-postgres-migration-data','data_generation/AutoDebitSchedule/AutoDebitSchedule-data1.csv','ap-south-1','aws-access-key', 'aws-secret-key')"

done
