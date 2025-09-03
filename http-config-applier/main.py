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
        consumer_group="http_config_applier",
        auto_create_topics=True,
        auto_offset_reset="earliest"
    )

    data_topic = app.topic(name=os.environ["input"], key_deserializer="str")
    output_topic = app.topic(name=os.environ["output"])
    sdf = app.dataframe(topic=data_topic)
    sdf.apply(config_apply).to_topic(output_topic, key=lambda row: row["machine"])
    app.run()


# It is recommended to execute Applications under a conditional main
if __name__ == "__main__":
    main()
