# Wheel CI 

**Simplest** CI solution for GCE Host VM <br>

> Due to **permission of GCP** <br>
> We have to **build** our own **CI server** <br>

> [!NOTE]
> 
> We have try the following CI solution <br>
> - **Github Action with GCP**
>   - no permission to add **Work Identity Pool** to **GCP** <br>
>   - no permission to add **Service Account** to **GCP** <br>
>   - no permission to **Cloud Build** <br>
> - **Github Action + SSH**
>    - no permission to add **SSH key** to **GCP** <br>
> - **Drone CI**
>    - no permission to **deploy cloud run** <br>

## Solution

- **Github Action + Wheel CI**
  - **Github Action** to **build** and **push** image to our **docker registry** <br>
  - **Wheel CI** to **deploy** image to **GCE Host VM** <br>

## Wheel CI Architecture

- Pipeline Runner 
    - monitor **new task** from **`tasks`** folder
    - run **`yaml/{new_task}.yaml`**
- Wheel CI Server
    - **webhook** to **trigger** **runner** to run **new task**

## Usage

### Setup

on GCE Host VM : 
```bash
make init # create `logs` `yaml` `tasks` folder
docker compose up -d # start wheel ci server
```

for **pipline runner** : 
```bash
python3 -m venv venv # create virtual environment
source venv/bin/activate # activate virtual environment
pip3 install pyyaml==6.0.1 # the only dependency pipleline runner need
python3 runner/run.py # start pipeline runner
```
> run `python3 runner/run.py` in **`screen`** or **`tmux`** <br>

enjoy ! <br>

### Pipeline YAML

add your **CI Pipeline** to **`yaml`** folder <br>

Format : 
- **name** : name of your CI Pipeline ( type : `string` )
- **steps** : steps of your CI Pipeline ( type : `array` )
    - **steps.name** : name of your step ( type : `string` )
    - **steps.commands** : commands of your step ( type : `array` )

Example Wheel CI yaml format : 
```yaml
name: Hello World of Wheel CI
steps:
  - name: Stop current container
    commands:
      - docker stop hello-world
  - name: Remove current container
    commands:
      - docker rm hello-world
  - name: Pull current image
    commands:
      - docker pull hello-world
  - name: Run new container
    commands:
      - docker run -d --name hello-world -p 80:80 hello-world
```

### Webhook

endpoint : `/api/v1/webhook/github/service/{service_name}` <br>
method : `POST` <br>
body :
```json
{
    "token" : "your_token"
}
```
- **service_name** : name of your service ( type : `string` )
    - should be same as **`yaml/{service_name}.yaml`** <br>
- **token** : token of your service ( type : `string` )

When **`POST`** request to **`/api/v1/webhook/github/service/{service_name}`** <br>
Wheel CI will **run** **`yaml/{service_name}.yaml`** <br>