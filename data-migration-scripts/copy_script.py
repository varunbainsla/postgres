from datetime import datetime

import boto3
# os.environ["PGPASSWORD"] = "nira12345"
print("start : ", datetime.now())

# AWS credentials and bucket names
aws_access_key_id = ''
aws_secret_access_key = ''
# source_bucket_name = 'new-temp-nira-data-lake'
source_bucket_name = 'nira-postgres-migration-data'
# source_bucket_name = 'new-temp-nira-data-lake'
# destination_bucket_name = 'new-temp-nira-data-lake'
# destination_folder = 'data_generation'
# table_name = 'AutoDebitSchedule'

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

folders = [
        # 'table_dump/AutoDebitSchedule/AWSDynamoDB/01711089712651-ffd29005/data/',
        # 'table_dump/User_Bank_detail/AWSDynamoDB/01711089739374-1f26cfaa/data/',
        # 'table_dump/User_Aadhaar/AWSDynamoDB/01711089737574-623660d7/data/',
        # 'table_dump/PaymentDue/AWSDynamoDB/01711089733863-3854cfc2/data/',
        # 'table_dump/Ops_Disbursal/AWSDynamoDB/01711089812070-86f1e775/data/'
        # 'table_dump/Loan/AWSDynamoDB/01711089730020-13170702/data/',
        'data_generation/User_Bank_detail/'
        ]

for source_folder in folders :
        response = s3.list_objects_v2(Bucket=source_bucket_name, Prefix=source_folder)
        for obj in response['Contents']:
            file_key = obj['Key']
            # Define the command to run
            command = f'''psql -h nira-test-db.cae5esa57zww.ap-south-1.rds.amazonaws.com -p 5432 -U postgres -d nira-test-db  -c "SELECT aws_s3.table_import_from_s3('public."AutoDebitSchedule"', 'identifier,"Item"', '(format csv, header true)','nira-postgres-migration-data','data_generation/AutoDebitSchedule/AutoDebitSchedule-data1.csv','ap-south-1','aws-access-key', 'aws-secret-key')" '''
            print(command)

            # subprocess.run(command, shell=True, check=True)