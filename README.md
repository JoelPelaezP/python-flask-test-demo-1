# Migrations
## Migration with flask_sqlalchemy
Run docker services (deatached mode)

`docker compose up --build --force-recreate --no-deps -d`

Generate Migration Script (flask app needs to be running) Development mode

`docker-compose exec <flask-app-service> flask db migrate -m "Initial migration"`


## Migration with Alembic

`alembic` as a database migration tool.

1. Install `alembic` package
```sh
pip install alembic
```

2. Initialize `alembic` in workspace, it will generate folder and `alembic.ini` file in specific folder
```sh
alembic init database/migrations
```

3. Generate first script
```sh
alembic --config ./database/migrations/alembic.ini revision --autogenerate -m "custom_message"
```

4. Apply migrations to database
```sh
alembic --config ./database/migrations/alembic.ini upgrade head
```

# New Relic Integration

1. install new relic package using pip command

```sh
pip install newrelic
```

2. Generate newrelic configuration file
```sh
newrelic-admin generate-config <YOUR_LICENSE_KEY> newrelic.ini`
```

3. Integrate to your application
Initialize newrelic agent before running your app

```sh
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
```

4. Implement ENVIRONMENT logic for each environment, we need to set a group with specific config and values. sample for `development` env.
```sh
[newrelic:development]
monitor_mode = true
app_name = <app-name-for-dev-env>
```

5. Set license key per environment using the general APM environment variable 
```sh
NEW_RELIC_LICENSE_KEY = <license-key-for-app-name-for-specific-env>
```

# Pydantic Integration
Load environment variables dinamycally, a prefix is required

1. Install `pydantic-settings`
```sh
pip install pydantic-settings
```

2. Implement a class config

```sh
import pydantic_settings

class PydanticBaseSettings(pydantic_settings.BaseSettings):
    pass

class MyConfig(PydanticBaseSettings):
    my_secret:str

    class Config:
        env_prefix = "ANYPREFIX_"
```

3. Set environment variables values in your `.env` file for local testing
```sh
ANYPREFIX_MY_SECFRET=SuperSecretValue
```