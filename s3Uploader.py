import os
import sys
import subprocess
import time
import boto3
from tqdm import tqdm

# install boto3 if not installed.
try:
    import boto3
except ModuleNotFoundError:
    print("Install boto3 in python3")
    subprocess.call([sys.executable, "-m", "pip", "install", 'boto3'])
finally:
    import boto3

# install tqdm if not installed.
try:
    import tqdm
except ModuleNotFoundError:
    print("Install tqdm in python3")
    subprocess.call([sys.executable, "-m", "pip", "install", 'tqdm'])
finally:
    from tqdm import tqdm

class s3Uploader():

    def __init__(self, bucket_name=None, access_key=None, secret_key=None, 
                    endpoint_url=None, multipart_threshold=1, max_concurrency=1, verbose=True):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        self.verbose = verbose

        print("s3 resource is being accessed..")
        self.s3 = boto3.resource(
            's3', 
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key, 
            endpoint_url=endpoint_url
        )

        print("s3 client is being accessed..") 
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )

        print("s3 bucket is being accessed..") 
        self.bucket = self.s3.Bucket(bucket_name)
        print(">>> Done.")

        self.MB = 1024 ** 2
        self.config = boto3.s3.transfer.TransferConfig(
            multipart_threshold=multipart_threshold * self.MB,
            max_concurrency=max_concurrency
        )

    def get_bytes(self, t):
            '''
            utility function for tqdm progress bar.
            '''
            def inner(bytes_amount):
                t.update(bytes_amount)
            return inner

    def check_path_exists(self, path):        
        result = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=path, MaxKeys=1)
        return 'Contents' in result
    
    def remove_last_seperator(self, path):
        '''
        utility function for removing "/" or "\" seperator at the end of path not to create unnecessary path.        
        '''
        if path == "":
            pass
        elif path[-1] == "/" or path[-1] == "\\":
            path = path[:-1:]
        return path

    def upload_folder(self, src_path, dest_path):
        
        src_file_paths = []
        src_path = os.path.abspath(src_path).replace("\\", "/")
        for root, folders, files in os.walk(src_path):
            for file in files:
                src_file_paths.append(os.path.join(root, file).replace("\\", "/"))                
        base_folder = os.path.basename(os.path.normpath(src_path))
        base_file_paths = [base_folder + "/" + src_file_path.replace(src_path + "/", "") for src_file_path in src_file_paths]
        
        for src_file_path, base_file_path in zip(src_file_paths, base_file_paths):            
            file_size = os.path.getsize(src_file_path)
            file_name = os.path.basename(src_file_path)
            
            dest_path = self.remove_last_seperator(dest_path)
            if dest_path == "":
                destination_path = base_file_path
            else:
                destination_path = dest_path + "/" + base_file_path
        
            if self.verbose == True:
                print(">>> upload file : (Local) " + src_file_path + " -> (S3 Storage) " + destination_path)
                time.sleep(0.3)
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name, ascii=True) as t:
                    self.s3.meta.client.upload_file(src_file_path, self.bucket_name, destination_path, Config=self.config, Callback=self.get_bytes(t), ExtraArgs={'ACL':'public-read'}) 
            else:
                print(">>> upload file : (Local) " + src_file_path + " -> (S3 Storage) " + destination_path)
                self.s3.meta.client.upload_file(src_file_path, self.bucket_name, destination_path, Config=self.config, ExtraArgs={'ACL':'public-read'}) 
                print("Done.")
        
        
    def upload_file(self, src_path, dest_path):
        
        src_path = os.path.abspath(src_path)
        file_size = os.path.getsize(src_path)
        file_name = os.path.basename(src_path)
        
        dest_path = self.remove_last_seperator(dest_path)
        if dest_path == "":
            destination_path = file_name
        else:
            destination_path = dest_path + "/" + file_name

        if self.verbose == True:
            print(">>> upload file : (Local) " + src_path + " -> (S3 Storage) " + destination_path)
            time.sleep(0.3)
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name, ascii=True) as t:
                self.s3.meta.client.upload_file(src_path, self.bucket_name, destination_path, Config=self.config, Callback=self.get_bytes(t)) 
        else:
            print(">>> upload file : (Local) " + src_path + " -> (S3 Storage) " + destination_path)
            self.s3.meta.client.upload_file(src_path, self.bucket_name, destination_path, Config=self.config) 
