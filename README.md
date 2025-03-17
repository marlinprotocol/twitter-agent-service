# oyster-x-agent

AI agent that automates the process of sending tweets from an X account managed by Oyster.

## .env file
```
OPENAI_API_KEY=
USER_PASSWORD=
USERNAME=
USER_EMAIL=
USER_EMAIL_PASSWORD=
X_APP_NAME=
```

## Running the twitter-agent & verifier

```
docker-compose up
```

## Deploy setup 

#### Debug
```
./oyster-cvm deploy --operator **** --wallet-private-key ****  --pcr-preset base/blue/v1.0.0/arm64 --duration-in-minutes 20 --debug --no-stream --docker-compose docker-compose.yml --init-params "xagent/.env:1:0:file:./.env"
```

#### Production
```
./oyster-cvm deploy --operator **** --wallet-private-key ****  --pcr-preset base/blue/v1.0.0/arm64 --duration-in-minutes 20 --docker-compose docker-compose.yml --init-params "xagent/.env:1:1:file:./.env"
```

## Generate access token and api keys
```
curl 127.0.0.1:8000/generate_keys_and_access_tokens
```

`Note` : This can take upto 15-20mins.

## Fetch access tokens and api keys
```
curl 127.0.0.1:8000/fetch_keys_and_tokens
```

## Verify encumbrance
```
curl 127.0.0.1:8888/verify_encumbrance
```

#### This endpoint provides the following guarantees:
1. The password for the Twitter account is known only to the enclave.
2. The password for the email account is known only to the enclave.
3. The Twitter account cannot be recovered as there is no backup email and the email matches the provided email ID.
4. There is only one app on the X developer portal, and its name matches the enclave-provided app name.
5. The access tokens and API keys for the twitter account were regenerated.

## TODO

- [x] X password reset.
- [x] Password and recovery phrase reset for tuta email-id.
- [x] Generating access token for api access with X developer portal.
- [x] Interface to get access tokens and api keys.
- [x] KMS integration for the password generation.
- [ ] Enclave setup


