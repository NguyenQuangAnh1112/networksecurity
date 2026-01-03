import logging
import os
from datetime import datetime


"""
    - tạo ra file log có tên gắn liền với thời gian thực
    - tự động tạo thư mục log nếu chưa có
    - cấu hình định dạng nội dung log
"""

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

"""
%(asctime)s: Thời gian xảy ra sự kiện.

%(lineno)d: Dòng code số bao nhiêu gây ra log này (rất hữu ích để debug).

%(name)s: Tên logger.

%(levelname)s: Mức độ (INFO, ERROR...).

%(message)s: Nội dung thông báo bạn viết.
"""

logger = logging.getLogger()
