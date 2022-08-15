# s3bucket_finder

## To run this feature, just follow the following instructions

### --| First, create a virtual environment and install all dependencies inside

    virtualenv .venv

    source .venv/bin/activate

    pip install -r requirements.txt

### --| After that, you just need to run the following instructions...

#### => For scanning a simple bucket

    python main.py scan -s BUCKET_NAME

Where BUCKET_NAME is the name of bucket you want to scan.

#### => For scanning a file containing a list of buckets name

    python main.py scan -sf FILE

Where the FILE parameter can be a file or a path to a file.

The generated CSV file of the scan are saved in your home working directory, is automatically created in ResultsCSV folder.
but you can change


#### => For scanning a simple bucket

    python main.py scan -s BUCKET_NAME --rename RENAME -p --path your_path_folder

#### => For scanning a file containing a list of buckets name

    python main.py scan -sf FILE --rename RENAME -p or --path your_path_folder

it doesn't matter if you give a relative path because when you give that your folder is create automaticaly in start of
home folder but if you specify a path that the parent folder has not exist the folder has not create


The file will have the name <rapport_aws_s3>, but you can give another name with the command --rename.


#### => For scanning a simple bucket

    python main.py scan -s BUCKET_NAME --rename RENAME

#### => For scanning a file containing a list of buckets name

    python main.py scan -sf FILE --rename RENAME

Where RENAME is the name of the generated CSV file.

## To set up your local AWS settings, follow the following instructions

* First, you need to have an AWS account.
* Then you need to type the following commands to configure your local settings:

        python main.py setup-config --region REGION [--output OUTPUT]

The previous command allows you to configure your region provided by AWS, you replace the REGION parameter by the name
of your region. For example: af-south-1 is ours. The OUTPUT parameter is optional.

        python main.py setup-cred --id AWS_ACCESS_KEY_ID --key AWS_SECRET_ACCESS_KEY

This command allows you to configure your credentials, you must provide your AWS access key id and your AWS secret
access key provided by AWS.
