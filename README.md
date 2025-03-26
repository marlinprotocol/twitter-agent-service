# twitter-agent-service

An AI agent service that securely exposes Twitter API keys and access tokens for a encumbered Twitter account within an Oyster Enclave, enabling other services inside the enclave to make verifiable tweets.

## Running the twitter agent service locally

1. Create environment variables files with all the required details
   ## .env file
   ```
   USERNAME=
   USER_EMAIL=
   X_APP_NAME=
   KMS_ENDPOINT=http://kms_imitator:1100
   AGENT_HOST=0.0.0.0
   ```

   ## .env.secrets
   ```
   OPENAI_API_KEY=
   USER_PASSWORD=
   USER_EMAIL_PASSWORD=
   ```

2. Build and run locally
   ```
   docker build -t twtagent .
   ```

   ```
   docker-compose up --build
   ```

3. Generate access token and api keys inside the enclave
   ```
   curl 127.0.0.1:8000/generate_keys_and_access_tokens
   ```

   >**Note** : This can take upto 15-20mins.

4. Fetch access tokens and api keys inside the enclave
   ```
   curl 127.0.0.1:8000/fetch_keys_and_tokens
   ```

5. Verify encumbrance
   ```
   curl 127.0.0.1:8888/verify_encumbrance
   ```



## Integrating twitter agent service into your enclave application

1. Create environment variables files with all the required details
   ## .env file
   ```
   USERNAME=
   USER_EMAIL=
   X_APP_NAME=
   ```

   ## .env.secrets
   ```
   OPENAI_API_KEY=
   USER_PASSWORD=
   USER_EMAIL_PASSWORD=
   ```

2. Include the following services and volume in your docker-compose.yml
   ```yaml
   twitter_agent_service:
      image: sagarparker/twitter_agent_service_amd64:latest
      init: true
      restart: unless-stopped
      network_mode: host
      command: ["/opt/venv/bin/python", "/app/x_agent.py"]
      volumes:
         - /init-params/:/init-params/
         - shared_data:/app/shared_data
      env_file:
         - /init-params/.env
         - /init-params/.env.secrets
   verifier:
      image: sagarparker/twitter_agent_service_amd64:latest
      init: true
      restart: unless-stopped
      network_mode: host
      command: ["/opt/venv/bin/python", "/app/verifier.py"]
      volumes:
         - /init-params/:/init-params/
         - shared_data:/app/shared_data
      env_file:
         - /init-params/.env
         - /init-params/.env.secrets
      
   volumes:
      shared_data:
   ```

3. In your application generate and retrieve access tokens securely within Oyster Enclaves using the following endpoints

   ```
   curl 127.0.0.1:8000/generate_keys_and_access_tokens
   ```


   ```
   curl 127.0.0.1:8000/fetch_keys_and_tokens
   ```

4. Deploy your application with oyster-cvm using the following command
   ```bash
   ./oyster-cvm deploy --wallet-private-key *** --pcr-preset base/blue/v1.0.0/amd64 --duration-in-minutes 45 --docker-compose docker-compose.yml --operator **** --instance-type r6i.xlarge --image-url https://artifacts.marlin.org/oyster/eifs/base-blue_v1.0.0_linux_amd64.eif --init-params ".env:1:1:file:.env" --init-params ".env.secrets:0:1:file:.env.secrets"
   ```
   >**Note** : You can specify init parameters for your application by adding more --init-params flags to your command.

5. Verify encumbrance using the following endpoint
   ```
   curl {oyster_enclave_ip}:8888/verify_encumbrance
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
- [x] Enclave setup


