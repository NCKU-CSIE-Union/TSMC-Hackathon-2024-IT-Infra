# Drone CI/CD setup

## Setup Ngrok

### Install Ngrok in Ubuntu

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```

### Add Ngrok token

```bash
ngrok config add-authtoken <token>
```

### Run Ngrok in background

```bash
ngrok http 8080 --log=stdout  > log &
```

### Get Ngrok URL

```bash
cat log | grep "url=" | awk '{print $8}' | awk -F "=" '{print $2}'
```

## Create a GitHub OAuth application

- Go to GitHub Settings > Developer settings > OAuth Apps (either in your personal account or in an organization), and register a new OAuth application.
- For example:
  - Application name: drone
  - Homepage URL: <https://drone.example.com>
  - Authorization callback URL: <https://drone.example.com/login>
  - if you use ngrok, the callback URL should be `https://<ngrok_url>/login`, home page URL should be `https://<ngrok_url>`
- create a client secret and copy it to the clipboard

### Disable third-party application restrictions(optional if you want to add the private repository in drone)

- Document: <https://docs.github.com/en/organizations/managing-oauth-access-to-your-organizations-data/disabling-oauth-app-access-restrictions-for-your-organization>

## Set up Drone

### Setup Drone server

we can use docker-compose that place in `ci/setup/drone/docker-compose.yml` to setup drone server
then you only need to change the following environment variables:

```env
DRONE_GITHUB_CLIENT_ID=<place your github oauth application client id here>
DRONE_GITHUB_CLIENT_SECRET=<place your github oauth application client secret here>
DRONE_SERVER_PROXY_HOST=<same as the github oauth application homepage url>
```

### Run Drone server

```bash
cd ci/setup/drone
docker-compose up -d
```

## reference

- <https://docs.drone.io/server/ha/developer-setup/>
- <https://github.com/Jim-Chang/KodingWork/blob/master/devops/painless_set_up_drone_ci_cd/docker-compose.yml>
- <https://koding.work/painless-set-up-drone-ci-cd/>
- <https://ithelp.ithome.com.tw/articles/10235164>
- <https://ithelp.ithome.com.tw/articles/10235165>
