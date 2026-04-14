# TO BE Implemented

# Migrations
1. Run docker services
`docker compose up --build --force-recreate --no-deps -d`

2. Generate Migration Script (flask app needs to be running):
`docker-compose exec <flask-app-service> flask db migrate -m "Initial migration"`


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
`license_key = <license-key-for-app-name-for-dev-env>`
