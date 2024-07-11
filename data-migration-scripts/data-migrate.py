import psycopg2
from psycopg2 import sql



# PostgreSQL connection parameters
# db_host = 'nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com'
# db_port = '5432'
# db_name = 'postgres'
# db_user = 'postgres'
# db_password = 'nira12345'
# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='nira12345',
    host='nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com',
    port='5432'
)

# aws_access_key = ''
# aws_secret_access_key = ''
# bucket_name = 'nira-postgres-migration-data'
# folder_prefix = 'data_generation/AutoDebitSchedule/'
# Create a cursor
cur = conn.cursor()

# Construct the SQL command to import data from S3
query = sql.SQL("""
    SELECT aws_s3_copy_manager.table_import_from_s3(
        'public."AutoDebitSchedule"',
        'identifier,"Item"',
        '(format csv, header true)',
        %s,
        %s,
        'ap-south-1',
        %s,
        %s
    )
""")

# Execute the query to import data from S3 to the table
cur.execute(query, ('nira-postgres-migration-data', 'data_generation/AutoDebitSchedule/AutoDebitSchedule-data1.csv', 'aws-access-key', 'aws-secret-key'))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()


SELECT aws_s3.table_import_from_s3('public."AutoDebitSchedule"', 'identifier,"Item"', '(format csv, header true)','nira-postgres-migration-data','data_generation/AutoDebitSchedule/AutoDebitSchedule-data1.csv','ap-south-1','aws-access-key', 'aws-secret-key')

psql - h
nira - test - db.cae5esa57zww.ap - south - 1.
rds.amazonaws.com - p
5432 - U
postgres - d
postgres - c
'SELECT
aws_s3.table_import_from_s3('public."AutoDebitSchedule"', 'identifier,"Item"', '(format csv, header true)',
                            'nira-postgres-migration-data',
                            'data_generation/AutoDebitSchedule/AutoDebitSchedule-data1.csv', 'ap-south-1',
                            'aws-access-key', 'aws-secret-key')'


psql -h nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com -p 5432 -U postgres -d nira-test-db -c "SELECT aws_s3.table_import_from_s3('public.\"AutoDebitSchedule\"', 'identifier,\"Item\"', '(format csv, header true)','nira-postgres-migration-data','data_generation/AutoDebitSchedule/AutoDebitSchedule-data1.csv','ap-south-1','aws-access-key', 'aws-secret-key')"

psql -h nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com -p 5432 -U postgres -d nira-test-db -W pswd nira12345 -c "SELECT aws_s3.table_import_from_s3('public."User_Bank_detail"', '"bankID","Item"', '(format csv, header true)','nira-postgres-migration-data','data_generation/User_Bank_detail/User_Bank_detail-data1.csv','ap-south-1','aws-access-key', 'aws-secret-key')"