import logging
import logging.config


def get_logger(file_name):
    print("Filename", file_name)
    return logging.getLogger(file_name)


def init(file_name):
    logging.basicConfig(
        level=logging.INFO,  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Print logs to console
            # logging.FileHandler("app.log") # Save logs to a file
        ],
    )
