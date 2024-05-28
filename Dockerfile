FROM python:3.10-slim
COPY etl_project/requirements.txt .
RUN pip install dagster \
    dagster-webserver \
    dagster-postgres \
    dagster-docker \
    dagster-dbt \
    pandas \
    polars \
    connectorx \
    pyarrow \
    psycopg2-binary \
    adbc_driver_manager \
    adbc-driver-postgresql

# Add repository code
WORKDIR /opt/dagster/app
COPY etl_project/etl_project/ etl_project/workspace.yaml /opt/dagster/app/
RUN mkdir /tmp/data/
# Run dagster gRPC server on port 4000
EXPOSE 4000
# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
# CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "pipeline"]
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "4000"]
