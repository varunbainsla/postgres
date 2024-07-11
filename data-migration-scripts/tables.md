# Tables Info



## script setup 
* dev ec2 :postgres-ec1
* run specific script for each table
* for bash run permission : chmod +x script-name.sh



## Postgres psql command
```commandline
\d+ : for table size
\l+ : for total datbase size

```

* ## User 
  * Primary key : userID
  * Indexes :

|           index-name           |    key-1 |    key-2    |
|:------------------------------:|:--------:|:-----------:|
| cognitoUserID-index  | cognitoUserID|      -      |
|deviceIdentifier-index|deviceIdentifier|      -      |
|isPartner-createdDate-index|  isPartner| createdDate |
|mobileNo-index|  mobileNo |      -      |
|officialEmailID-index|  officialEmailID |      -      |
|panNumber-index|panNumber|      -      |
|personalEmailID-index|personalEmailID|      -      |


* ## Loan
    * Primary Key : loanID
    * Indexes :


|           index-name           |    key-1 |     key-2     |
|:------------------------------:|:--------:|:-------------:|
| productType-createdDate-index  | productType |  createdDate  |
|     tag-updatedDate-index	     |tag|  updatedDate  |
|transactionIdentifier-index|  transactionIdentifier |       -       |
|userID-index|  userID |       -       |
|visibleLoanID-loanStartDate-index|  visibleLoanID | loanStartDate |







