import logging
from time import time, localtime

from quota_tracker.options import QuotaOptions
from quota_tracker.utils import read_json, write_to_json


class QuotaTracker(object):
    def __init__(self,
                 filename: str,
                 max_quota: int,
                 dir_path: str = "./",
                 options: QuotaOptions = QuotaOptions(),
                 logger=None):

        if not logger:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('QuotaTracker')
        else:
            self.logger = logger

        self.options = options
        self.dir_path = dir_path
        self.filename = filename
        try:
            read_json(f"{self.dir_path}/{self.filename}")
        except FileNotFoundError:
            write_to_json(
                _dir=self.dir_path,
                filename=self.filename,
                data={"timestamp": int(time()), "count": self.options.start_quota},
                mode='w'
            )

        self._refresh_quota()
        self.max_quota = max_quota
        self.current_quota = self._load_current_quota()

    def _load_current_quota(self):
        log = read_json(f"{self.dir_path}/{self.filename}")
        return log.get("count")

    def _save_count(self):
        log = {"timestamp": int(time()), "count": self.current_quota}
        write_to_json(self.dir_path, self.filename, log)

    def get_current_quota(self):
        return self.current_quota

    def count_request(self, num=1):
        self.current_quota += num
        self._save_count()

    def show_status(self):
        self.logger.info(f'CurrentQuota: {self.get_current_quota()}/{self.max_quota}')

    def _refresh_quota(self):
        log = read_json(f"{self.dir_path}/{self.filename}")
        log_time = localtime(log.get("timestamp"))
        now_time = localtime(time())
        if self.options.refresh_by == "month" and (now_time.tm_mon > log_time.tm_mon) or \
                self.options.refresh_by == "day" and (now_time.tm_mday > log_time.tm_mday):
            self.current_quota = 0
            self._save_count()

    def is_exceeded_quota(self):
        if self.current_quota < self.options.warning_rate * float(self.max_quota):
            self.logger.info("QuotaStatus: OK")
        elif self.current_quota < self.max_quota:
            self.logger.info(f"QuotaStatus: WARNING - Exceeded {self.options.warning_rate * 100}% of quota requests")
        else:
            self.logger.info(f"QuotaStatus: STOPPING - Exceeded 100% of quota requests")
            return True
        return False
