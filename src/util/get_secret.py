import json

from botocore.exceptions import ClientError


def get_secret(sm_client, secret_id):
    try:
        response = sm_client.get_secret_value(SecretId=secret_id)
        decoded = json.loads(response["SecretString"])
        return decoded
    except ClientError as e:
        print(e)
        raise e
