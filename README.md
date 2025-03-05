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
python3 twtagent.py
```

## Generate access token endpoint
```
curl 127.0.0.1:5000/get_access_tokens
```

## TODO

- [x] X password reset.
- [x] Password and recovery phrase reset for tuta email-id.
- [x] Generating access token for api access with X developer portal.
- [ ] Interface to send tweets.
- [ ] KMS integration
- [ ] Enclave setup


