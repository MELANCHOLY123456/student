"""
应用日志配置
为整个应用设置统一的日志管理
"""

import logging
import os
from config import Config


def configure_logging():
    """
    配置应用的日志系统

    日志将输出到：
    1. 控制台 (console)
    2. 文件 (logs/app.log)
    """
    # 确保日志目录存在
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 获取根logger
    root_logger = logging.getLogger()
    root_logger.setLevel(Config.LOG_LEVEL)

    # 格式化器
    formatter = logging.Formatter(Config.LOG_FORMAT)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 文件处理器
    file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # 抑制第三方库的过多日志
    logging.getLogger('mysql').setLevel(logging.WARNING)
    logging.getLogger('mysql.connector').setLevel(logging.WARNING)

    root_logger.info(f"日志系统初始化完成, 级别: {Config.LOG_LEVEL}")


if __name__ == '__main__':
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("测试日志消息")
