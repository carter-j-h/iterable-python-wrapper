# IterableWrapper
Python Wrapper for the Iterable API, more details coming soon

## Installation

pip install iterablepythonwrapper

## Setup

pip install -r requirements.txt

## Usage:

```python
from iterablepythonwrapper.client import IterableAPI

APIKEY="ENTER YOUR API CREDENTIALS HERE"

ic = IterableAPI(api_key=APIKEY)
```

## Campaigns

Create Campaign: (https://api.iterable.com/api/docs#!/campaigns/create_campaign)

```python
ic.create_campaign(name="Weekly Newsletter", list_ids=[77675], template_id=300987,
				   send_at="01-01-2018 09:00:00", send_mode="ProjectTimeZone",
				   data_fields={"productRecommendation1": "iPhone X",
				   				"productRecommendation2": "MacBook Pro",
				   				"productRecommendation3": "Apple TV"})
```

## Commerce

Update Cart: (https://api.iterable.com/api/docs#!/commerce/updateCart)

```python

ic.update_cart()
```

Track Purchase (https://api.iterable.com/api/docs#!/commerce/trackPurchase)

```python
ic.track_purchase()
```

