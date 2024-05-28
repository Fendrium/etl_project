stop:
	docker-compose down

build_project: stop
	docker build -t pipeline:latest .

run:
	docker-compose --env-file .env up -d

build_run: build_project run

load_data:
	chmod +x ./load_data_b2b.sh
	./load_data_b2b.sh
run_and_load: run load_data


restart: stop run
