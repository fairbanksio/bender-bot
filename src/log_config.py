import logging, os, sys

# Create the formatter
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Create a StreamHandler and add the formatter to it
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

# Configure your logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG if os.environ.get("DEBUG") else logging.INFO)
