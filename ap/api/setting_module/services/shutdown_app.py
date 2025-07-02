import logging
import os
from time import sleep

from flask import request

from ap.common.constants import REMOTE_DATA_FILE_NAME, AnnounceEvent
from ap.common.logger import log_execution_time
from ap.common.multiprocess_sharing import EventBackgroundAnnounce, EventQueue, EventShutDown
from ap.script.disable_terminal_close_button import close_terminal

logger = logging.getLogger(__name__)


@log_execution_time()
def shut_down_app():
    logger.info('///////////// SHUTDOWN APP ///////////')
    EventQueue.put(EventBackgroundAnnounce(data=True, event=AnnounceEvent.SHUT_DOWN))
    EventQueue.put(EventShutDown())
    logging.shutdown()
    sleep(5)

    # close terminal
    close_terminal()

    shutdown_function = request.environ.get('werkzeug.server.shutdown')
    if shutdown_function is not None:
        shutdown_function()

    for ext in (".csv", ".tsv"):
        if os.path.exists(REMOTE_DATA_FILE_NAME + ext):
            os.remove(REMOTE_DATA_FILE_NAME + ext)
            logger.info("Removed temporary remote data file of type: " + ext)

    os._exit(0)
