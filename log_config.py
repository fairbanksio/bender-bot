import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG if os.environ.get("DEBUG") else logging.INFO)