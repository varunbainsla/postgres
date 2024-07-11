import time
from datetime import datetime

import boto3
import pandas as pd
import os
import gzip
import csv
from dynamodb_json import json_util as json_b
import json
import swifter


import uuid



table_key = {
    'Loan' : 'loanID',
    'LoanStatus' : 'loanID',
    'Ops_Disbursal' : 'loanID',
    'PaymentDue': 'loanHistoryID',
    'User_Aadhaar':'userID',
    'User_Bank_detail':'bankID',
    'AutoDebitSchedule':'identifier',
    'BankReference':'bankCode',
    'Configuration':'key',
    'User':'userID'



             }
def uuid_version(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)
        return uuid_obj.version
    except ValueError:
        return 'None'

def decompress_gzip_file(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(f_in.read())


def ddb_json_to_json(rec):
    try :
        data = json_b.loads(rec)
        return data
    except :
        return None

def json_to_jsondump(rec):
    try :
        return json.dumps(rec)
    except :
        return None

def validate_pk(rec):
    if table_name in ['AutoDebitSchedule'] and table_name_key =='AutoDebitSchedule_identifier' and rec.get('identifier') is not None and uuid_version(rec['loanID']) not in [ None,'null','None','none']:
        return f'{rec["identifier"]}'
    elif table_name in ['AutoDebitSchedule'] and table_name_key =='AutoDebitSchedule_loanID' and rec.get('identifier') is not None and uuid_version(rec['loanID']) not in [ None,'null','None','none']:
        return f'{rec["loanID"]}'

    elif table_name in ['User_Bank_detail'] and rec.get('bankID') is not None and uuid_version(rec['bankID']) !='None':
        return f'{rec["bankID"]}'

    elif table_name in ['User_Aadhaar'] and rec.get('userID') is not None and uuid_version(rec['userID']) !='None':
        return f'{rec["userID"]}'

    # elif table_name in ['PaymentDue'] and rec.get('loanHistoryID') is not None and uuid_version(rec['loanID']) !='None':

        # return f'{rec["loanHistoryID"]}',f'{rec["loanID"]}'
    elif table_name in ['PaymentDue'] and  table_name_key =='PaymentDue_loanID' and rec.get('loanID') is not None and uuid_version(rec['loanID']) !='None':
        return f'{rec["loanID"]}'
    elif table_name in ['PaymentDue'] and  table_name_key =='PaymentDue_loanHistoryID' and rec.get('loanHistoryID') is not None and uuid_version(rec['loanHistoryID']) !='None':
        return f'{rec["loanHistoryID"]}'



    elif table_name in ['Ops_Disbursal'] and rec.get('loanID') is not None and uuid_version(rec['loanID']) !='None':
        return f'{rec["loanID"]}'

    elif table_name in ['LoanStatus'] and  table_name_key =='LoanStatus_loanID' and rec.get('loanID') is not None and uuid_version(rec['loanID']) !='None':
        return f'{rec["loanID"]}'
    elif table_name in ['LoanStatus'] and  table_name_key =='LoanStatus_loanState' and rec.get('loanID') is not None and uuid_version(rec['loanID']) !='None':
        return f'{rec["loanState"]}'
    elif table_name in ['Loan'] and rec.get('loanID') is not None and uuid_version(rec['loanID']) !='None':
        return f'{rec["loanID"]}'

# ------------ BANK REFERENCE TABLE ----
    elif table_name in ['BankReference'] and  table_name_key =='BankReference_createdDate' and rec.get('createdDate') is not None :
        return f'{rec["createdDate"]}'
    elif table_name in ['BankReference'] and  table_name_key =='BankReference_bankCode' and rec.get('bankCode') is not None :
        return f'{rec["bankCode"]}'

# ----------- USER TABLE---
    elif table_name in ['User'] and  table_name_key =='User_userID' and rec.get('userID') is not None and uuid_version(rec['userID']) !='None':
        return f'{rec["userID"]}'

# ------------- CONFIGURATION TABLE
    elif table_name in ['Configuration'] and  table_name_key =='Configuration_key' and rec.get('key') is not None :
        return f'{rec["key"]}'
    # elif  uuid_version(rec['identifier']) not in [ None,'null','None','none']:
    #     return rec['identifier']
    else :
        return 'None'



def process_data_file(input_file, count, table_name):

    # Load data from JSON file
    global table_name_key
    df = pd.read_json(input_file, lines=True)
    df['Item'] = df['Item'].swifter.apply(ddb_json_to_json)  #map(json.loads(i))
    global table_name_key
    if table_name in ['LoanStatus']:
        table_name_key = table_name + '_loanState'
        df['loanState'] = df['Item'].swifter.apply(validate_pk)

        table_name_key = table_name + '_loanID'
        df['loanID'] = df['Item'].swifter.apply(validate_pk)

    elif table_name in ['User']:
        table_name_key = table_name + '_userID'
        df['userID'] = df['Item'].swifter.apply(validate_pk)

    elif table_name in ['BankReference']:
        table_name_key = table_name + '_createdDate'
        df['createdDate'] = df['Item'].swifter.apply(validate_pk)
        table_name_key = table_name +'_bankCode'
        df['bankCode'] = df['Item'].swifter.apply(validate_pk)

    elif table_name in ['Configuration']:
        table_name_key = table_name + '_key'
        df['key'] = df['Item'].swifter.apply(validate_pk)



    elif table_name in ['AutoDebitSchedule']:
        # global table_name_key
        table_name_key = table_name + '_loanID'
        df['loanID'] = df['Item'].swifter.apply(validate_pk)

        table_name_key = table_name + '_identifier'
        df['identifier'] = df['Item'].swifter.apply(validate_pk)

    elif table_name in ['PaymentDue']:
        # global table_name_key
        table_name_key = table_name + '_loanHistoryID'
        df['loanHistoryID'] = df['Item'].swifter.apply(validate_pk)

        table_name_key = table_name + '_loanID'
        df['loanID'] = df['Item'].swifter.apply(validate_pk)

    # elif table_name in ['PaymentDue']:
    #     table_name= table_name +'_loanHistoryID'
    #     df['loanHistoryID']= df['Item'].swifter.apply(validate_pk)
    #     table_name_key = table_key + '_loanID'
    #     df['loanID'] = df['Item'].swifter.apply(validate_pk)
    else :
        df[f'{table_key[table_name]}'] = df['Item'].swifter.apply(validate_pk)
    df['Item'] = df['Item'].swifter.apply(json_to_jsondump)
    # if table_name in ['Loan','LoanStatus','Ops_Disbursal']:
    #     df[f'{table_key[table_name]}'] = df['Item'].swifter.apply(get_loanID)
    # elif table_name in ['PaymentDue']:
    #     df[f'{table_key[table_name]}'] = df['Item'].swifter.apply(get_loanID)
    # elif table_name in ['User_Aadhaar']:
    #     df[f'{table_key[table_name]}'] = df['Item'].swifter.apply(get_loanID)
    # elif table_name in ['User_Bank_detail'] :
    #     df[f'{table_key[table_name]}'] = df['Item'].swifter.apply(get_loanID)

    column_list = df.columns.to_list()
    new_df = df[column_list[::-1]]
    new_df = new_df[new_df[f'{table_key[table_name]}'] != 'None']
    file_name = f'{table_name}-data{count}.csv'

    new_df.to_csv(file_name,index=False)
    # Filter rows with valid UUIDs
    # valid_uuids = df[df['userid'].apply(lambda x: isinstance(x, str) and uuid.UUID(x, version=4))]

    # Convert data to desired format
    # formatted_data = []
    # for index, row in valid_uuids.iterrows():
    #     formatted_data.append({'userid': row['userid'], 'item': row.to_dict()})

    return file_name



def save_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [f'{table_key["table_name"]}', 'Item']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def upload_to_s3(local_file, key):
    # s3 = boto3.client('s3')
    aws_access_key_id = ''
    aws_secret_access_key = ''
    # source_bucket_name = 'new-temp-nira-data-lake'
    bucket_name = 'nira-postgres-migration-data'
    # source_folder = 'table_dump/AutoDebitSchedule/AWSDynamoDB/01711089712651-ffd29005/data/'
    # destination_folder = 'data_generation/AutoDebitSchedule/'

    # Initialize S3 client
    s3_dev = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3_dev.upload_file(local_file, bucket_name, key)
    print("file upload success :",local_file)


def main():
    print("start : ",datetime.now())
    # AWS credentials and bucket names
    aws_access_key_id = ''
    aws_secret_access_key = ''
    source_bucket_name = 'new-temp-nira-data-lake'
    destination_bucket_name = 'new-temp-nira-data-lake'
    destination_folder = 'data_generation'
    # table_name = 'AutoDebitSchedule'

    # Initialize S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    folders = [
        'table_dump/User/AWSDynamoDB/01712774249656-501b1b21/data/',
        # 'table_dump/BankReference/AWSDynamoDB/01711089741213-4b61f3fc/data/',
        # 'table_dump/Configuration/AWSDynamoDB/01711089735748-a4545d13/data/',
        # 'table_dump/AutoDebitSchedule/AWSDynamoDB/01711089712651-ffd29005/data/',
        # 'table_dump/User_Bank_detail/AWSDynamoDB/01711089739374-1f26cfaa/data/', --
        # 'table_dump/User_Aadhaar/AWSDynamoDB/01711089737574-623660d7/data/', --
        # 'table_dump/PaymentDue/AWSDynamoDB/01711089733863-3854cfc2/data/',
        # 'table_dump/Ops_Disbursal/AWSDynamoDB/01711089812070-86f1e775/data/'
        # 'table_dump/Loan/AWSDynamoDB/01711089730020-13170702/data/' --,
        # 'table_dump/LoanStatus/AWSDynamoDB/01711089731975-16c43ff5/data/' --
        ]

    for source_folder in folders :

        # List files in source folder
        response = s3.list_objects_v2(Bucket=source_bucket_name, Prefix=source_folder)
        count =1
        global table_name
        table_name = source_folder.split('/')[1]
        print(table_name ," : time taken : " ,datetime.now())
        # Process each file
        for obj in response['Contents']:
            file_key = obj['Key']
            filename = os.path.basename(file_key)

            # Download file from S3
            local_file =  filename
            s3.download_file(source_bucket_name, file_key, local_file)

            # Decompress the file if it's in .gz format
            if filename.endswith('.gz'):
                decompressed_file = local_file[:-3]
                decompress_gzip_file(local_file, decompressed_file)
                os.remove(local_file)
                local_file = decompressed_file

            # Process the data
            csv_file = process_data_file(local_file,count,table_name)
            count =count+1

            # Save the formatted data to a CSV file
            # csv_file =  filename.replace('.json.gz', '.csv')
            # save_to_csv(formatted_data, csv_file)
            #
            # # Upload the CSV file to the destination S3 bucket
            destination_key = f"{destination_folder}/{table_name}/{csv_file}"
            # destination_key = csv_file
            upload_to_s3(csv_file, destination_key)
            #
            # Remove the CSV file from local storage
            os.remove(local_file)
            os.remove(csv_file)
            #
            # # Remove the local decompressed file
            # if filename.endswith('.gz'):
            #
    print(datetime.now())


if __name__ == "__main__":
    main()
