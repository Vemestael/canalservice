# canalservice

## About

Test assignment for Canalservice

## Installation and using

This project provides you a working Django environment without requiring you to install Python/Django, a web server, and any other server software on your local machine. For this, it requires Docker and Docker Compose.

1. Install [Docker](https://docs.docker.com/engine/installation/) and [Docker-compose](https://docs.docker.com/compose/install/);

2. Clone this project and then cd to the project folder;

3. Create your own .env file by copying .env.example:
    ```sh
    $ cp src/.env.example src/.env
    ```

4. Update the environment variables in the docker-compose.yml and .env files.

5. Build the images and run the containers:
     ```sh
    $ docker-compose -f docker-compose.yml up -d --build
    ```

6. You've done! Main page is available on http://localhost

7. After finishing work, you can stop running containers:
    ```sh
    $ docker-compose down
    ```

## Testing

To start parsing data from Google Sheets, go to http://localhost/gsheets

After running the script, you will be redirected to http://localhost/order-list to view the obtained data

If you change the data in Google Sheets, go to http://localhost/gsheets again to retrieve the changed data

## Other

To test using the webhook, you need to deploy the application on a server with the domain

1. Create an nginx configuration file to handle ssl:
    ```sh
    $ mkdir conf.d
    $ cp ./Docker/nginx/nginx.prod.conf ./conf.d/nginx.conf
    ```

2. Update the environment variables in the docker-compose.yml, conf.d/nginx.conf files

3 Add the following variable to the .env file
```
CSRF_TRUSTED_ORIGINS=https://your_web_site
```

3. Set up a webhook for your site with Apix-Drive.com

4. Build the images and run the containers:
     ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

5. You've done! Main page is available on https://your_web_site

You can see a finished example at https://vemestael.ru

Web hook goes off once every half hour on a schedule