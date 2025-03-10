# oyster-x-agent

AI agent that automates the process of sending tweets from an X account managed by Oyster.

## .env file
```
OPENAI_API_KEY=
USER_PASSWORD=
USERNAME=
USER_EMAIL=
USER_EMAIL_PASSWORD=
KMS_GENERATED_PASSWORD=
X_APP_NAME=
```

## Running the twitter-agent

```
python3 main.py
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
curl 127.0.0.1:8000/verify_encumbrance
```

## TODO

- [x] X password reset.
- [x] Password and recovery phrase reset for tuta email-id.
- [x] Generating access token for api access with X developer portal.
- [x] Interface to get access tokens and api keys.
- [ ] KMS integration for the password generation.
- [ ] Enclave setup


