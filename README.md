# Quota Tracker

A small package for quota tracking when using third party's APIs (such as RapidAPI).

## QuickStart

Installation:

```commandline
pip install quota-tracker
```

Simple use:

```python
from quota_tracker import QuotaTracker

tracker = QuotaTracker(filename="quota_log.json", max_quota=1000)
```

## Custom Options

Current support options:

| Default option       | Description                                                          |
|----------------------|----------------------------------------------------------------------|
| `refresh_by="month"` | Quota will be restart to `0` automatically for each `month` or `day` |
| `start_quota=0`      | Set an initial quota                                                 |
| `warning_rate=0.8`   | Set a warning rate for watching in logger                            |

Example:
```python
from quota_tracker import QuotaTracker
from quota_tracker.options import QuotaOptions

options = QuotaOptions(start_quota=0,
                       refresh_by="month",
                       warning_rate=0.8)

tracker = QuotaTracker(filename="quota_log.json",
                       max_quota=1000,
                       options=options)
```

## Custom Logger:

Example:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MyQuotaTracker')

from quota_tracker import QuotaTracker
tracker = QuotaTracker(filename="quota_log.json",
                       max_quota=1000,
                       logger=logger)
```

# License

MIT License - Copyright (c) 2022 Thi Dang