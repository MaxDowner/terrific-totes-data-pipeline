import json

from botocore.exceptions import ClientError


def get_secret(sm_client, secret_id: str):
    """Retrieve secret from aws secret manager.

    Args:
        sm_client (boto3): boto3 secret manager client
        secret_id (str): secret that is stored in AWS secret manager

    Raises:
        e: _client error message

    Returns:
        dict: decoded secret file
    """
    try:
        print(f'getting secret {secret_id}')
        response = sm_client.get_secret_value(SecretId=secret_id)
        print(f'response is {response}')
        decoded = json.loads(response["SecretString"])
        return decoded
    except ClientError as e:
        print(e)
        raise e
