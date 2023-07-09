import logging
import sys

logger = logging.getLogger("runweb")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
