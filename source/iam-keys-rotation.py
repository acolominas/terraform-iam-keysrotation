import boto3
from botocore.exceptions import ClientError
import datetime
import json
import os

iam_client = boto3.client('iam')
sm_client = boto3.client('secretsmanager')

def list_access_key(user, days_filter, status_filter):
    keydetails=iam_client.list_access_keys(UserName=user)
    key_details={}
    user_iam_details=[]

    # Some user may have 2 access keys.
    for keys in keydetails['AccessKeyMetadata']:
        if (days:=time_diff(keys['CreateDate'])) >= days_filter and keys['Status']==status_filter:
            key_details['UserName']=keys['UserName']
            key_details['AccessKeyId']=keys['AccessKeyId']
            key_details['days']=days
            key_details['status']=keys['Status']
            user_iam_details.append(key_details)
            key_details={}

    return user_iam_details

def time_diff(keycreatedtime):
    now=datetime.datetime.now(datetime.timezone.utc)
    diff=now-keycreatedtime
    return diff.days

def create_key(username):
    access_key_metadata = iam_client.create_access_key(UserName=username)
    access_key = access_key_metadata['AccessKey']['AccessKeyId']
    secret_key = access_key_metadata['AccessKey']['SecretAccessKey']
    return access_key,secret_key

def disable_key(access_key, username):
    try:
        iam_client.update_access_key(UserName=username, AccessKeyId=access_key, Status="Inactive")
        print(access_key + " has been disabled.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)

def delete_key(access_key, username):
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print (access_key + " has been deleted.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)

def store_key(access_key,secret_key,username):
    json_data=json.dumps({'AccessKey':access_key,'SecretKey':secret_key})
    try:
        sm_client.put_secret_value(SecretId="iam/"+username,SecretString=json_data)
        print (access_key + " has been stored.")
    except ClientError as e:
        print("The access key with id %s cannot be stored" % access_key)


def lambda_handler(event, context):

    users = os.environ["USERS"].split(",")
    days = int(os.environ["DAYS"])
    for user in users:
        user_iam_details=list_access_key(user=user,days_filter=days,status_filter='Active')
        for _ in user_iam_details:
            disable_key(access_key=_['AccessKeyId'], username=_['UserName'])
            delete_key(access_key=_['AccessKeyId'], username=_['UserName'])
            access_key,secret_key = create_key(username=_['UserName'])
            store_key(access_key,secret_key,username=_['UserName'])

    return {
        'statusCode': 200,
        'body': list_access_key(user=user,days_filter=0,status_filter='Active')
    }
