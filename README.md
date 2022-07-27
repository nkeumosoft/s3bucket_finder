# s3bucket_finder

## To run this script, you must first have configured your local AWS settings. 
* First of all, you need to have an AWS account
* Then you need to type the following commands to configure your local settings:

        python main.py setup-config --region REGION [--output OUTPUT]
The previous command allows you to configure your region provided by AWS, you replace the REGION parameter by the name of your region. For example: af-south-1 is ours.
The OUTPUT parameter is optional.

        python main.py setup-cred --id AWS_ACCESS_KEY_ID --key AWS_SECRET_ACCESS_KEY
This command allows you to configure your credentials, you must provide your AWS access key id and your AWS secret access key provided by AWS.

* When the configurations are done, you can now launch the main script
* 
        python main.py -f your file-name
* Example  file-name = first.txt this file content 10 words that you can use or also can use bucket_test.txt it content more than 5000 words for your own test just run

        python main.py -f first.txt
        
        python main.py -f bucket_test.txt

Following this command, a directory named ResultsCSV will be created in your home directory and will contain the report_aws_s3.csv file.