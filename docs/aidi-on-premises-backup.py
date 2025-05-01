# Script to backup Aidi on-premises.
# Contact your Aidi customer representative to obtain your location, your access key and your secret key.
from datetime import datetime
import os
from pathlib import Path
import sys
from typing import Any
import click
import boto3
from tqdm import tqdm

def __connect_to_s3(aidi_backup_bucket: str, aidi_backup_access_key: str, aidi_backup_secret_key: str) -> Any:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aidi_backup_access_key,
        aws_secret_access_key=aidi_backup_secret_key,
    )
    pretty_print(f'Attempting to connect to bucket "{aidi_backup_bucket}"')
    try:
        s3.head_bucket(Bucket=aidi_backup_bucket)
        pretty_print(f'Connection successful to bucket "{aidi_backup_bucket}"')
    except Exception as e:
        __exit_app(f'Error: Failed to connect to S3 bucket "{aidi_backup_bucket}" with access key "{aidi_backup_access_key}" and secret key "{__obfuscate(aidi_backup_secret_key)}". Check your source bucket parameter, access key and secret key. Detailed error: "{str(e)}"')

    return s3

def __create_path(target_directory: str, force_create_directory: bool):
    dir_exists = os.path.isdir(target_directory)
    if not dir_exists and not force_create_directory:
        __exit_app(reason=f'Error: The directory "{target_directory}" does not exist. Create the directory or run this script with "--force-create-directory true"')
    elif not dir_exists:
        try:
            Path(target_directory).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            __exit_app(reason=f'Error: Failed to create the directory "{target_directory}". Detailed error: "{str(e)}"')

def __download_files(s3_client: Any, target_directory: str, aidi_backup_bucket: str, number_of_files: int, overwrite_existing_files: bool):
    response = s3_client.list_objects_v2(Bucket=aidi_backup_bucket)
    pretty_print(f'Starting the download of files from the "{aidi_backup_bucket}" bucket.')

    progress_bar = tqdm(total=number_of_files, unit=" files")
    counter = 0

    continuation_token = None
    has_more_entries = True

    while has_more_entries:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=aidi_backup_bucket, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=aidi_backup_bucket)

        if "Contents" not in response:
            break 

        for obj in response["Contents"]:
            key = obj["Key"]
            __download_file(s3_client=s3_client, key=key, aidi_backup_bucket=aidi_backup_bucket, target_directory=target_directory, overwrite_existing_files=overwrite_existing_files)

            progress_bar.update(1)

            if counter % 10 == 0:
                progress_bar.set_description(f'Downloaded: {__truncate(key)}')

            counter = counter + 1

            if counter >= number_of_files: 
                break

        if response.get("IsTruncated"):
            continuation_token = response["NextContinuationToken"]
        else:
            break

    progress_bar.close()
    pretty_print(f'Finished the download of {counter} files from the "{aidi_backup_bucket}" bucket.')

def __download_file(s3_client: Any, key: str, aidi_backup_bucket:str, target_directory: str, overwrite_existing_files: bool):
    file_location = os.path.join(target_directory, key)
        
    if "/" in key:
        Path(os.path.dirname(file_location)).mkdir(parents=True, exist_ok=True)

    if overwrite_existing_files == True or not Path(file_location).exists():
        s3_client.download_file(aidi_backup_bucket, key, file_location)

def __count_files_in_bucket(s3_client: Any, aidi_backup_bucket: str) -> int:
    count = 0
    pretty_print(f'Obtaining the number of files in the bucket "{aidi_backup_bucket}". This may take a few seconds...')
    continuation_token = None
    has_more_entries = True

    while has_more_entries:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=aidi_backup_bucket, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=aidi_backup_bucket)

        if "Contents" in response:
            count += len(response["Contents"])

        if response.get("IsTruncated"):
            continuation_token = response["NextContinuationToken"]
        else:
            has_more_entries = False

    pretty_print(f'There are {count} files in the "{aidi_backup_bucket}" bucket.')
    return count

def __exit_app(reason: str):
    pretty_print(reason)
    exit(1) 

def pretty_print(message: str):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}: {message}', flush=True)

def __obfuscate(plan_text: str) -> str:
    return f'{plan_text[:3] + "*" * (len(plan_text) - 3)}'

def __truncate(long_text: str) -> str:
    return ('...' + long_text[-47:]) if len(long_text) > 50 else long_text.rjust(50)

@click.command()
@click.option(
    "-b", "--aidi-backup-bucket", 
    required=True,
    type=str,
    help=" Name of the bucket to fetch data from. Given by your Aidi customer service representative. The command must be executed once per bucket to backup. Example: `backup-fs-my-environment-name`."
)
@click.option(
    "-a", "--aidi-backup-access-key", 
    required=True,
    type=str,
    help="Access key as given by your Aidi customer service representative. Example: `ABCDEFGHIJ1234567890`"
)
@click.option(
    "-s", "--aidi-backup-secret-key", 
    required=True,
    envvar="AIDI_BACKUP_SECRET_KEY",
    hide_input=True,
    type=str, 
    help="Secret key as given by your Aidi customer service representative. Can also be provided using the the `AIDI_BACKUP_SECRET_KEY` environment variable for improved security, if not provided as a command-line argument. Example: `aBcDeFgHiJkLmNoPqRsTuVwXyZ+1234567890123`"
)
@click.option(
    "-t", "--target-directory", 
    required=True,
    type=str, 
    help="The target directory where the backup should be located. Example: `/tmp/backup-2025-02-08`"
)
@click.option(
    "-f", "--force-create-directory", 
    type=bool,
    default=False,
    help="Whether the directory (and all its parents) should automatically be created or not if they do not exist. May exit if this script is not given permission to create the directory. Defaults to `false`."
)
@click.option(
    "-o", "--overwrite-existing-files", 
    type=bool,
    default=False,
    help="Overwrites the downloaded files if they do not already exist. Defaults to `false`."
)
def backup(aidi_backup_bucket: str, aidi_backup_access_key: str, aidi_backup_secret_key: str, target_directory: str, force_create_directory: bool, overwrite_existing_files: bool):
    '''
    Aidi On-Premise Backup script

    Generates a backup of your Aidi instance locally. Is essentially a wrapper for a boto3 connection to an AWS S3 bucket. 

    This script is meant to backup your Aidi instance locally. It is not meant to extract or manipulate Aidi's data. The structure and content of the data returned by this script may change over time without notice. 
    As a result, the data returned by this script should not be used for business logic, reporting, or any other application beyond backups. Aidi is not responsible for any issues arising from the use of this script outside its intended purpose.

    '''
    pretty_print(f'Starting backup with following parameters:')
    pretty_print(f'Aidi Backup Bucket:          {aidi_backup_bucket}')
    pretty_print(f'Aidi Backup Access Key:      {aidi_backup_access_key}')
    pretty_print(f'Aidi Backup Secret Key:      {__obfuscate(aidi_backup_secret_key)}')
    pretty_print(f'Target Directory:            {target_directory}')
    pretty_print(f'Force Create Directory:      {force_create_directory}')
    pretty_print(f'Overwrite Existing Files:    {overwrite_existing_files}')

    __create_path(target_directory=target_directory, force_create_directory=force_create_directory)
    s3_client = __connect_to_s3(aidi_backup_bucket=aidi_backup_bucket, aidi_backup_access_key=aidi_backup_access_key, aidi_backup_secret_key=aidi_backup_secret_key)
    number_of_files = __count_files_in_bucket(s3_client=s3_client, aidi_backup_bucket=aidi_backup_bucket)
    __download_files(s3_client=s3_client, target_directory=target_directory, aidi_backup_bucket=aidi_backup_bucket, number_of_files=number_of_files, overwrite_existing_files=overwrite_existing_files)

if __name__ == '__main__':
    backup()
