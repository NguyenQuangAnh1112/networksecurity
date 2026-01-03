import sys
from networksecurity.logging.logger import logger


def error_message_detail(error, error_detail):
    _, _, exc_traceback = error_detail.exc_info()

    # lấy tên file code đang bị lỗi
    file_name = exc_traceback.tb_frame.f_code.co_filename

    # lấy dòng code đang bị lỗi
    line_number = exc_traceback.tb_lineno

    error_message = f"Error occurred in python script name [{file_name}] line_number [{line_number}] error message [{str(error)}]"

    return error_message


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details):
        self.error_message = error_message_detail(
            error=error_message, error_detail=error_details
        )

        super().__init__(self.error_message)


if __name__ == "__main__":
    try:
        logger.info(f"Start testing Exception Handling...")
        a = 1 / 0
    except Exception as e:
        logger.info(f"not devine 0")
        raise NetworkSecurityException(e, sys)
