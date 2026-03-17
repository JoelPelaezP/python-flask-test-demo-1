FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD [ "flask", "run", "--host", "0.0.0.0" ]


# docker command to run app
# 1.1. build docker image
# docker build -t <image-name> .
# 1.2. run docker image
# docker run -p 5005:5000 <image-name>
# 2. run app with reload option to detect changes and rebuild the app using volumes
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" <image-name>

# docker compose commands to run app
# 1. run app
# docker compose up
# 2. force to recreate with new env variables or configurations
# docker compose up --build --force-recreate --no-deps <app_name>
# 3. debug with docker compose (respect other docker compose files)
# docker compose -f docker-compose.yml -f docker-compose.debug.yml up
 