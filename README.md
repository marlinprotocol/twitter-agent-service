# oyster-x-agent

An AI agent service that securely exposes Twitter API keys and access tokens for a encumbered Twitter account within an Oyster Enclave, enabling other services inside the enclave to make verifiable tweets.

## .env file
```
OPENAI_API_KEY=
USER_PASSWORD=
USERNAME=
USER_EMAIL=
USER_EMAIL_PASSWORD=
X_APP_NAME=
```

> `Note` : Add `KMS_ENDPOINT=http://kms_imitator:1100` to the `.env` file if testing on local.

## Running the twitter-agent & verifier locally

```
docker build -t twtagent .
```

```
docker-compose up --build
```

## Deploy on oyster

#### Install oyster-cvm by following the official guide


https://docs.marlin.org/oyster/build-cvm/quickstart

#### Deploy in debug mode 
`WARNING` : This exposes environment variables, which may pose security risks. Proceed with caution.
```
./oyster-cvm deploy --wallet-private-key ****** --pcr-preset base/blue/v1.0.0/amd64 --duration-in-minutes 45 --debug --no-stream --docker-compose docker-compose-prod.yml --operator ****** --instance-type r6i.xlarge --image-url https://artifacts.marlin.org/oyster/eifs/base-blue_v1.0.0_linux_amd64.eif --init-params "xagent/.env:0:0:file:.env"
```

#### Deploy in production mode
```
./oyster-cvm deploy --wallet-private-key ***** --pcr-preset base/blue/v1.0.0/amd64 --duration-in-minutes 45 --docker-compose docker-compose-prod.yml --operator ***** --instance-type r6i.xlarge --image-url https://artifacts.marlin.org/oyster/eifs/base-blue_v1.0.0_linux_amd64.eif --init-params "xagent/.env:0:1:file:.env"
```

## Generate access token and api keys inside the enclave
```
curl 127.0.0.1:8000/generate_keys_and_access_tokens
```

`Note` : This can take upto 15-20mins.

## Fetch access tokens and api keys inside the enclave
```
curl 127.0.0.1:8000/fetch_keys_and_tokens
```

## Verify encumbrance
```
curl {oyster_enclave_ip}:8888/verify_encumbrance
```

#### This endpoint provides the following guarantees:
1. The password for the Twitter account is known only to the enclave.
2. The password for the email account is known only to the enclave.
3. The Twitter account cannot be recovered as there is no backup email and the email matches the provided email ID.
4. There is only one app on the X developer portal, and its name matches the enclave-provided app name.
5. The access tokens and API keys for the twitter account were regenerated.


## Steps to Make a Tweet Using the Test Application

Follow these steps to securely generate secrets and make a tweet using the test application:

1. **Generate Secrets Inside the TEE**  
   Use the following API call to generate the necessary secrets inside the Trusted Execution Environment (TEE):  
   ```bash
   curl {oyster_enclave_ip}:7000/generate_secrets_for_encumbered_account
   ```
   > **Note**: This API call does not return the API keys or tokens. It only initializes the secrets securely within the enclave.

2. **Make a Tweet**  
   Use the following endpoint to make a tweet from the encumbered account:  
   ```bash
   curl {oyster_enclave_ip}:7000/make_tweet_from_encumbered_account
   ```
   This endpoint ensures that the tweet is made securely using the secrets stored in the enclave.

## TODO

- [x] X password reset.
- [x] Password and recovery phrase reset for tuta email-id.
- [x] Generating access token for api access with X developer portal.
- [x] Interface to get access tokens and api keys.
- [x] KMS integration for the password generation.
- [x] Enclave setup
- [x] Application to make a tweet


