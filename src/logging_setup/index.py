import os
import logging
from datetime import datetime

def setup_logging(log_dir, log_level):
    """
    设置日志配置，输出日志到文件和控制台。

    参数：
    log_dir: 日志文件输出目录。
    log_level: 日志级别。
    """
    os.makedirs(log_dir, exist_ok=True)
    log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')
    log_path = os.path.join(log_dir, log_filename)
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_path, filemode='w')

    # 控制台输出日志
    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
