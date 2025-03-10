import json

from botocore.exceptions import ClientError


def get_secret(sm_client, secret_id):
    '''Retrieve secret from aws secret manager.'''
    try:
        print(f'getting secret {secret_id}')
        response = sm_client.get_secret_value(SecretId=secret_id)
        print(f'response is {response}')
        decoded = json.loads(response["SecretString"])
        return decoded
    except ClientError as e:
        print(e)
        raise e
