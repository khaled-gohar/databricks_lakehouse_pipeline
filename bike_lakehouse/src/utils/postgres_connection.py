from dotenv import load_dotenv
import os



load_dotenv(
    "/Workspace/Users/kahledtrojan@gmail.com/databricks_lakehouse_pipeline_de/bike_lakehouse/config/dev/secrets/.env"
)


def get_postgres_properties():

    jdbc_url = (
        f"jdbc:postgresql://{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DATABASE")}"
    )



    properties = {
        "user": os.getenv("POSTGRES_USERNAME"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }


    return jdbc_url, properties