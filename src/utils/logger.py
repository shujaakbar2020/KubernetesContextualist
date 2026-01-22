import sys
import structlog
import logging

def setup_logging(level: str = "INFO"):
    """
    Configures structlog for structured JSON output in production 
    and pretty-printed output for local development.
    """
    
    # Standard Python logging sync
    # Use stderr for MCP servers to avoid corrupting JSON-RPC messages on stdout
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
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
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),  # Use stderr for MCP stdio compatibility
        cache_logger_on_first_use=True,
    )

# Create a global logger instance
logger = structlog.get_logger()