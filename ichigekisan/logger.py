from logging import Formatter, handlers, getLogger
from pathlib import Path


class Logger:
    def __init__(self, root_dir, level, name=__name__,):
        self.logger = getLogger(name)
        self.logger.setLevel(level)
        self.level = level
        formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

        # /[root_dir]/log/[app_name]/[app_name].logに出力
        root_dir = Path(root_dir)
        dir_name = root_dir.name
        log_dir = Path.joinpath(Path(root_dir).resolve(), 'log')
        # logフォルダ無かったら作成
        if not log_dir.is_dir():
            Path.mkdir(log_dir)
        filename = '{}/{}.log'.format(log_dir, dir_name)

        handler = handlers.RotatingFileHandler(
            filename=filename,
            maxBytes=1048576,
            backupCount=3,
            encoding='utf-8'
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def logging(self, msg):
        if self.level == 10:
            self.logger.debug(msg)
        elif self.level == 20:
            self.logger.info(msg)
        elif self.level == 30:
            self.logger.warning(msg)
        elif self.level == 40:
            self.logger.error(msg)
        elif self.level == 50:
            self.logger.critical(msg)
