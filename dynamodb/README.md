# DynamoDB

We will start from installing standalone DynamoDB client for a local testing

   SSH to EC2 instance (refer to Aurora)

   cd
   mkdir dynamodb
   cd dynamodb

   wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz

   tar -xzf dynamodb_local_latest.tar.gz
   java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

   Task:
   - add Inbound rule allowing you to connect from your IP to port 8000

   Navigate in your browser to:
   enpoint-ip.compute-1.amazonaws.com:8000/shell

   Go through the tutorial and discuss

Create a live DynamoDB tables

   https://console.aws.amazon.com/dynamodb/

   Table: ProductCatalog
   Primary key, in the Partition key: Id
   Data type: Number
   Read/Write capacity: 1/1

   Table: Forum
   PK: Name / String

   Table: Thread
   PK: ForumName / String
   Add sort key: Subject / String

   Table: Reply
   PK: Id / String
   SK: ReplyDateTime / String

   Amazon Linux AMI comes with preinstalled AWS SDK, when using different server follow:
   http://docs.aws.amazon.com/cli/latest/userguide/installing.html

   Open IAM: https://console.aws.amazon.com/iam/
   Create IAM user: training-dynamodb
   Note Access Key ID/Secret Access Key
   Attach policy to user

   $ aws configure

   Configure:
   AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
   AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   Default region name [None]: us-east-1
   Default output format [None]: ENTER

   Default output format: json, text, or table (default json)

   Download sample data:
   wget http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/samples/sampledata.zip
   unzip sampledata.zip

   aws dynamodb batch-write-item --request-items file://ProductCatalog.json
   aws dynamodb batch-write-item --request-items file://Forum.json
   aws dynamodb batch-write-item --request-items file://Thread.json
   aws dynamodb batch-write-item --request-items file://Reply.json

   Verify data was imported correctly (Items tab):
   https://console.aws.amazon.com/dynamodb/

   Query Reply Items, ID: Amazon DynamoDB#DynamoDB Thread 1









