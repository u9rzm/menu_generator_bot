DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yml
NGINX_FILE = docker_compose/nginx.yml
APP_CONTAINER = menu_for_bars
NGINX_CONTAINER = nginx_bar
TBUILD_FILE = docker_compose/test_build.yml

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d
.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down
#______________________________________________
.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

#Nginx
.PHONY: nginx
nginx:
	${DC} -f ${NGINX_FILE} up --build -d
.PHONY: nginx-logs
nginx-logs:
	${LOGS} ${NGINX_CONTAINER} -f
.PHONY: nginx-exec
nginx-exec:
	${EXEC} ${NGINX_CONTAINER} -f
.PHONY: nginx-down
nginx-down:
	${DC} -f ${NGINX_FILE} down

#Tests
.PHONY: btest
btest:
	${DC} -f ${TBUILD_FILE} ${ENV} up --build -d
	
.PHONY: btest-down
btest-down:
	${DC} -f ${TBUILD_FILE} down

.PHONY: test
test:
	${EXEC} ${NGINX_CONTAINER} pytest

.PHONY: all
all:
	${DC} -f ${NGINX_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: test
test:
	${EXEC} ${NGINX_CONTAINER} pytest