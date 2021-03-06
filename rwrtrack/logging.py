"""Provides some boiler-plate logging configuration management functions."""
import sys
import logging
import logging.config


logger = logging.getLogger(__name__)


def _configure_logging(log_conf_path, log_path, args):
    """Configure logging from the file configuration, output path, and verbosity control args."""
    log_opts = {"logfilename": log_path.as_posix(), "consoleloglvl": "INFO"}

    if args.get("-q", None):
        log_opts["consoleloglvl"] = "ERROR"
    elif args.get("-v", None):
        log_opts["consoleloglvl"] = "DEBUG"

    logging.config.fileConfig(log_conf_path.as_posix(), disable_existing_loggers=False, defaults=log_opts)

    logger.debug(f"Logging configured from '{log_conf_path}'")
    logger.debug(f"Logging output will be written to '{log_path}'")
    logger.debug(f"Running rwrtrack.py with arguments: {sys.argv[1:]}")


def _mod_logging_handlers(handler_type, handler_level):
    """Modify the logging level of handler_type logging handlers to handler_level."""
    for handler in logging.getLogger().handlers:
        if isinstance(handler, handler_type):
            logger.info(f"Setting {handler} to {logging.getLevelName(handler_level)}")
            handler.setLevel(handler_level)
