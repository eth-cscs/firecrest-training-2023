current_dir := $(shell pwd)

build:
	docker image rm -f firecrest-live
	docker build -f ./docker/Dockerfile -t firecrest-live .
run:
	docker run --rm --ip 192.168.220.31 -p 9090:9090 -v ${current_dir}/log:/var/log -v ${current_dir}/ssl:/app/ssl  --name firecrest-live firecrest-live
stop:
	docker stop firecrest-live