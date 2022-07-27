# s3bucket_finder

## === > New Feature < ===

### To run this new feature, you don't need to configure something, just follow the following instructions

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
