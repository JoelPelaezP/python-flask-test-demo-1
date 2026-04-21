# TO BE Implemented

# Migrations
## Migration with flask_sqlalchemy
1. Run docker services
`docker compose up --build --force-recreate --no-deps -d`

2. Generate Migration Script (flask app needs to be running) Development mode
`docker-compose exec <flask-app-service> flask db migrate -m "Initial migration"`


## Migration with Alembic
1. Install `alembic` package
`pip install alembic`

2. Initialize `alembic` in workspace, it will generate folder and alembic.ini file in specific folder
`alembic init database/migrations`

3. Generate first script
`alembic --config ./database/migrations/alembic.ini revision --autogenerate -m "initial script"`

4. Apply migrations to database
`alembic --config ./database/migrations/alembic.ini upgrade head `
# New Relic Integration

1. install new relic package using pip command
`pip install newrelic`

2. Generate newrelic configuration file
`newrelic-admin generate-config <YOUR_LICENSE_KEY> newrelic.ini`

3. Integrate to your application
Initialize newrelic agent before running your app
`import newrelic.agent`
`newrelic.agent.initialize('newrelic.ini')`

4. Implement ENVIRONMENT logic for newrelic
For each environment we need to set a group with specific config and values, sample for development env.
`[newrelic:development]`
`monitor_mode = true`
`app_name = <app-name-for-dev-env>`

5. Set license key per environment using the general APM environment variable 
`NEW_RELIC_LICENSE_KEY = <license-key-for-app-name-for-specific-env>`
