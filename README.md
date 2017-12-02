# IterableWrapper
Python Wrapper for the Iterable API, more details coming soon

## Installation:

```python
from iterable_wrapper import IterableAPI

APIKEY="ENTER YOUR API CREDENTIALS HERE"

ic = IterableAPI(api_key=APIKEY)
```

###### Campaigns

List Campaign Info: (https://api.iterable.com/api/docs#!/campaigns/campaigns)

```python
ic.list_campaign_info()
```

