# ETL Project

This project is a small ETL project using the following architecture:

- B2B Platform hosted in a PostgreSQL database
- Dagster for data orchestration and processing
- Data Warehouse hosed in a 2nd PostgreSQL database

Additionally, there is a Python script and a few shell scripts to generate and preload simulated B2B data

## Usage

The project uses a Makefile to simplify the process

1. Launch Docker Desktop
2. Building the B2B Docker image

```bash
make build_project
```

4. Run the containers

```bash
make run
```

3. Loading the data in the B2B DB

```bash
make load_data
```

4. Using Dagster UI to launch jobs
   [http://localhost:4000/]
