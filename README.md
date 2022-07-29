# s3bucket_finder

## === > Feature 1 < ===

### To run this feature, just follow the following instructions

### --| First, create a virtual environment and install all dependencies inside

    virtualenv .venv

    source .venv/bin/activate
    
    pip install -r requirements.txt

### --| After that, you just need to run the following instructions...

#### => For scanning a simple bucket

    python main.py --scrap-bucket BUCKET_NAME or python main.py -s BUCKET_NAME

Where BUCKET_NAME is the name of bucket you want to scan.

#### => For scanning a file containing a list of buckets name

    python main.py --scrap-file FILE or python main.py -sf FILE

Where the FILE parameter can be a file or a path to a file.

## === > Feature 2 < ===

### To run this feature, you must first have configured your local AWS settings. 
* First, you need to have an AWS account.
* Then you need to type the following commands to configure your local settings:

        python main.py setup-config --region REGION [--output OUTPUT]
The previous command allows you to configure your region provided by AWS, you replace the REGION parameter by the name of your region. For example: af-south-1 is ours.
The OUTPUT parameter is optional.

        python main.py setup-cred --id AWS_ACCESS_KEY_ID --key AWS_SECRET_ACCESS_KEY
This command allows you to configure your credentials, you must provide your AWS access key id and your AWS secret access key provided by AWS.

* When the configurations are done, you can now launch the feature 

#### => For scanning and download a acl properties with simple bucket into csv  file 

    python main.py --scrap-bucket BUCKET_NAME download or python main.py -s BUCKET_NAME  download 
    * if you have file who content a list of bucket just tape this in your terminal cmd
    python main.py --scrap-file FILE download or python main.py -sf FILE download -r | --rename your new rename file

#### by default the S3finder make a folder into your home directory with R
#### Where BUCKET_NAME is the name of bucket you want to scan.
    
    python main.py --scrap-bucket BUCKET_NAME download or python main.py -s BUCKET_NAME  download 
    * if you have file who content a list of bucket just tape this in your terminal cmd
    python main.py --scrap-file FILE download or python main.py -sf FILE download -r | --rename your new rename file

#### => For scanning a file containing a list of buckets name <<rapport_aws_s3>>
like a name but if you want to change this just tape
 
Where the FILE parameter can be a file or a path to a file.
