
### [Credentials guide for boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#guide-credentials)

There are two types of configuration data in Boto3: **credentials** and **non-credentials**. Credentials include items such as `aws_access_key_id`, `aws_secret_access_key`, and `aws_session_token`. Non-credential configuration includes items such as `region`, and s3 address style.

#### Credentials

Boto3 will look in several locations when searching for credentials, in order, and stops when one is found:
- Passing credentials as parameters in the `boto.client()` method
- Passing credentials as parameters when creating a Session object
- Environment variables
- Shared credential file (`~/.aws/credentials`)
- AWS config file (`~/.aws/config`)
- Assume Role provider
- Boto2 config file (`/etc/boto.cfg` and `~/.boto`)
- Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

> Note that hard-coding credentials is not recommended.

Envirenment vairables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` can be used. `AWS_SESSION_TOKEN` is used when using temporary credentials.

Example configuration file (default: `~/.aws/config` or `AWS_CONFIG_FILE`) with three profiles, `default`, `dev` and `prod`:
```ini
[default]
aws_access_key_id=foo
aws_secret_access_key=bar

[profile dev]
aws_access_key_id=foo2
aws_secret_access_key=bar2

[profile prod]
aws_access_key_id=foo3
aws_secret_access_key=bar3
```

There are other more advanced ways that use the config file (AWS Single Sign-On Provider).

`IAM roles` can also be used from inside EC2 if no other credential is provided. i.e. use the credentials given to the EC2 instance.

#### Other configurations
boto3 looks for configuration in either a `Config` object or `~/aws/config` file. 
> Note that astroquery.mast uses `Config`.

Some of the [configuration parameters](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html) include: `region_name`, `signature_version`, `s3`(-related things), `proxies`, etc. An example code is:

```python
my_config = botocore.config.Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
)
client = boto3.client('kinesis', config=my_config)
```
> Config does not take credentials keywords, nor a profile. These needs to be passed to `boto3.client` or `boto3.session.Session`


### Other tips:
- Clients
```python
# Create a low-level client with the service name
s3 = boto3.client('s3')

## or
# Get the client from the resource
s3_resource = boto3.resource('s3')
s3aw = sqs_resource.meta.client
```


### Tracking Cases:

- User in the cloud
    - Requested data in the cloud
        - User own cloud account
            - compute and data in same region:
                - s3 download.
            - compute and data *NOT* in same region:
                - anonymous user (no credentials)
                    - http download
                - cloud user (with credentials):
                    - cross-region transfer allowed:
                        - s3 download, requester pays
                    - cross-region transfer *NOT* allowed:
                        - warn, fall back to http download
        - User provided cloud account, i.e. platform
            - s3 download, compute and data are in the same region by design.
    - Requested data *NOT* in the cloud
        - http download

- User *NOT* in the cloud
    - http download.
    
    
> For http download, handle login or delegate to the relevant astroquery module

> s3 download, think about download cap?