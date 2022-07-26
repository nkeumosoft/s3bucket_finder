# s3bucket_finder

## === > New Feature < ===
### To run this new feature, you don't need to configure something, just follow the following instructions
### --| First, create a virtual environment and install all dependencies inside

>> virtualenv .venv

>> source .venv/bin/activate

>> pip install -r requirements.txt

### --| After that, you just need to run...

>> python main.py --scrap-bucket BUCKET_NAME or python main.py -s BUCKET_NAME

Where BUCKET_NAME is the name of bucket you want to scan.


## If you want to configure your local AWS settings, you just need to follow the following instructions
* First of all, you need to have an AWS account
* Then you need to type the following commands to configure your local settings:

        python main.py setup-config --region REGION [--output OUTPUT]
The previous command allows you to configure your region provided by AWS, you replace the REGION parameter by the name of your region. For example: af-south-1 is ours.
The OUTPUT parameter is optional.

        python main.py setup-cred --id AWS_ACCESS_KEY_ID --key AWS_SECRET_ACCESS_KEY
This command allows you to configure your credentials, you must provide your AWS access key id and your AWS secret access key provided by AWS.
