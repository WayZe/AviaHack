PROJECT_NAME = aviahack
PORTS = 5000:5000
DIR = "$(PWD)/data/:/code/data/"

build:
	docker build -t ${PROJECT_NAME} .

run:
	docker run -it -p ${PORTS} -v ${DIR} ${PROJECT_NAME} run

start:
	docker build -t ${PROJECT_NAME} .
	docker run -it -p ${PORTS} -v ${DIR} ${PROJECT_NAME} run
