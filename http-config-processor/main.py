# import the Quix Streams modules for interacting with Kafka.
# For general info, see https://quix.io/docs/quix-streams/introduction.html
from quixstreams import Application
from quixstreams.models.topics import Topic
from quixstreams.dataframe.joins.lookups import (
    QuixConfigurationService,
    QuixConfigurationServiceJSONField as Field
)

import os
from datetime import datetime

# for local dev, load env vars from a .env file
# from dotenv import load_dotenv
# load_dotenv()


def get_quix_config_lookup(topic: Topic) -> QuixConfigurationService:
    return QuixConfigurationService(
        topic=topic,
        broker_address=os.environ["Quix__Broker__Address"],
    )


def config_apply(row: dict) -> dict:
    """
    Applies the printer machine configs retrieved from QuixConfigurationManager.
    The config is a dict that looks like:
    {"editor_name": "The Editor", "mapping": {"T001": "sensor_1", "T002": "sensor_2"}, "field_scalar": .50}
    """
    final_row = {
        "machine": row.pop("machine"),
        "config_editor": row.pop("editor_name"),
        "timestamp": row.pop("timestamp"),
    }
    scalar = float(row.pop("field_scalar"))
    mapping = row.pop("mapping")
    for field_id in row.keys():
        final_row[mapping.get(field_id, field_id)] = row[field_id] * scalar
    return final_row


def main():
    # App setup
    app = Application(
        consumer_group="http_config_processor",
        auto_create_topics=True,
        auto_offset_reset="earliest"
    )

    data_topic = app.topic(name=os.environ["DATA_TOPIC"], key_deserializer="str")
    config_topic = app.topic(name=os.environ["CONFIG_TOPIC"])
    output_topic = app.topic(name=os.environ["output"])
    sdf = app.dataframe(topic=data_topic)

    # The QuixConfigurationService helps manage versioning of configs.
    # It communicates with the `Configuration API svc` to retrieve configs
    # based on a combination of message key and config "type".
    # The retrieved structure is templated (with the ability to customize as needed)
    # and for this example can be inspected in the `Machine Configuration UI` frontend.
    enricher = QuixConfigurationService(
        topic=config_topic,
        app_config=app.config,
    )

    # Enrich data using defined configs (lookup_join)
    sdf = sdf.join_lookup(
        lookup=enricher,
        fields={
            "editor_name": Field(
                type="printer-config",
                default=None,
                jsonpath="editor_name"
            ),
            "field_scalar": Field(
                type="printer-config",
                default=1.0,
                jsonpath="field_scalar"
            ),
            "mapping": Field(
                type="printer-config",
                default={},
                jsonpath="mapping"
            ),
        }
    ).apply(config_apply)

    # Finish off by writing to the final result to the output topic
    sdf.to_topic(output_topic, key=lambda row: row["machine"])

    # With our pipeline defined, now run the Application
    app.run()


# It is recommended to execute Applications under a conditional main
if __name__ == "__main__":
    main()
