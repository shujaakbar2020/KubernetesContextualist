import sys
import structlog
import logging

def setup_logging(level: str = "INFO"):
    """
    Configures structlog for structured JSON output in production 
    and pretty-printed output for local development.
    """
    
    # Standard Python logging sync
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # If we are in a TTY (terminal), use colorful pretty printing
    # If not (e.g., Docker/K8s), use JSON for machine readability
    if sys.stderr.isatty():
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Create a global logger instance
logger = structlog.get_logger()