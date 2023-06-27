import uuid
import logging
# console log handler
console_handler = logging.StreamHandler()
# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


def gen_uuid():
    # 生成基于时间戳和MAC地址的UUID
    uuid1 = uuid.uuid1()
    logger.info('gen uuid:%s', uuid1)
    return uuid1

 
