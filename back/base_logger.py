# inspired by https://stackoverflow.com/a/59559996/6352677

import logging as logginglevel

logginglevel.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    # level=loglevel,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logginglevel.getLogger(__name__)
logger.setLevel(logginglevel.INFO)
