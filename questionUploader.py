import os
import argparse
from s3Uploader import s3Uploader
import htmlParser
import uploadToServer

#############################################################
BUCKET_NAME = "nia-question-bucket"
ACCESS_KEY = "AKIAXQKSTMV4YCJDJAQ4"
SECRET_KEY = "HyPqaY9OFGeXsVh1gM2mGMhQogdhEFD83xqb6XaT"
SRC_PATH0 = "/Users/rubis/Desktop/Sample Problem/asset"
SRC_PATH1= "/Users/rubis/Desktop/Sample Problem/subquestions"
DEST_PATH = "/"
#############################################################

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', required=True, help="(Required) enter 'up' for upload or 'down' for download.")
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    
    args = get_args()
    s3Uploader = s3Uploader(
        bucket_name = BUCKET_NAME,
        access_key = ACCESS_KEY,
        secret_key = SECRET_KEY,
    )
    
    
    if args.subject == "math":
        s3Uploader.upload_folder(SRC_PATH0, DEST_PATH)
        htmlParser.getAttribute()
        s3Uploader.upload_folder(SRC_PATH1, DEST_PATH)
        uploadToServer.getAttribute()

    # elif args.subject == "korean":
    #     s3Uploader.upload_folder(SRC_PATH0, DEST_PATH)
    #     htmlParser.getAttribute()
    #     s3_updownloader.upload_folder(SRC_PATH1, DEST_PATH)
    #     uploadToServer.getAttribute() 

    # elif args.subject == "survey":
    #     s3Uploader.upload_folder(SRC_PATH0, DEST_PATH)
    #     htmlParser.getAttribute()
    #     s3_updownloader.upload_folder(SRC_PATH1, DEST_PATH)
    #     uploadToServer.getAttribute()       

