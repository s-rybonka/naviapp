# NaviApp
### Project setup.
#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms));
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/)).

#### Configuring the Environment
You can find all environment variables under ```docker/``` directory. This is how it looks like:
```bash
docker
├── app
│   ...
│   └── .env
└── db
    ...
    └── .env
```
Manually creation from ```envs.examples``` directory:
```bash
$ cp envs.example/app.env docker/app/.env
$ mkdir docker/db/ && cp envs.example/db.env docker/db/.env
```
### Build/Run Application
```bash
$ docker-compose up
$ docker-compose start
```
### Start Bot
```bash
$ docker-compose run --rm app python bot.py
```
### Start tests
```bash
$ docker-compose run --rm app pytest
```
### That's it.