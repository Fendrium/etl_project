from setuptools import find_packages, setup

setup(
    name="etl_project",
    packages=find_packages(exclude=["etl_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-postgres",
        "dagster-dbt",
        "pandas",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
