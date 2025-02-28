import json

from botocore.exceptions import ClientError


def get_secret(sm_client, secret_id):
    try:
        response = sm_client.get_secret_value(SecretId=secret_id)
        decoded = json.loads(response["SecretString"])
        # secret = response['SecretString']
        # base_dir = os.path.join(os.path.dirname())
        # file_path = base_dir / "secrets.txt"

        print(decoded)
        # use path dynamically instead of hardcoding?
        return decoded
    except ClientError as e:
        raise e
