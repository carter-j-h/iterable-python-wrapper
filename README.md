# IterableWrapper
Python Wrapper for the Iterable API.  Current version is 1.1

## Installation

```python

pip3 install iterablepythonwrapper

```

## Setup

```python

pip3 install -r requirements.txt

```

## Usage:

```python
from iterablepythonwrapper.client import IterableApi

APIKEY="ENTER YOUR API CREDENTIALS HERE"

ic = IterableApi(api_key=APIKEY)
```

## Campaigns

Create Campaign: (https://api.iterable.com/api/docs#!/campaigns/create_campaign)

```python
ic.create_campaign(name="Weekly Newsletter", list_ids=[80665], template_id=300987)
```

## Commerce

Track Purchase (https://api.iterable.com/api/docs#!/commerce/trackPurchase)

```python
cart_purchases = [
	{
		"id": "100",
		"sku": "1000",
		"name": "iPhone X",
		"description": "The latest iPhone with the biggest screen ever!",
		"categories":["mobile", "iPhone X", "Apple", ],
		"price": 999.99,
		"quantity": 1
	}
]

ic.track_purchase(user={"email":"jane.doe@gmail.com"}, items=cart_purchases, total=999.99)
```

Update Cart: (https://api.iterable.com/api/docs#!/commerce/updateCart)

```python
cart_items = [
	{
		"id": "100",
		"sku": "1000",
		"name": "iPhone X",
		"description": "The latest iPhone with the biggest screen ever!",
		"categories":["mobile", "iPhone X", "Apple", ],
		"price": 999.99,
		"quantity": 1
	}
]
ic.update_cart(user={"email": "john.doe@gmail.com"}, items=cart_items)
```

## Events

Track Event: (https://api.iterable.com/api/docs#!/events/track)
```python
event_details= {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X; rv:42.0) Gecko/20100101 Firefox/42.0",
	"referrer": "https://www.google.com"
}

ic.track_event(email="abe.lincoln@usa.gov",
				event_name="app_login",
				dataFields=event_details,
				campaign_id=215,
				template_id= 1000)
```

## Templates

Upsert Email Template (https://api.iterable.com/api/docs#!/templates/upsertEmailTemplate)

```python
ic.upsert_email_template(client_template_id=100000,
						name="New Email Template",
						from_name="Abe Lincoln",
						reply_to_email="abe.lincoln@usa.gov",
						subject="A word from Abe Lincoln!", 
						preheader_text="Abe wants You!",
						html=HTML_CONTENT_HERE)
```

## Users

Update User (https://api.iterable.com/api/docs#!/users/updateUser)

```python
ic.update_user(email="abe.lincoln@usa.gov",
				data_fields={"firstName":"Abe",
							"lastName":"Lincoln",
							"jobTitle": "16th President of the United States"})

```

Bulk Update (https://api.iterable.com/api/docs#!/users/bulkUpdateUser)

```python
presidents = [
	{
		"email": "abe.lincoln@usa.gov",
		"dataFields": {
			"firstName":"Abe",
			"lastName":"Lincoln",
			"jobTitle": "16th President of the United States"
		}
	},
	{
		"email": "theodore.Roosevelt@usa.gov",
		"dataFields": {
			"firstName":"Teddy",
			"lastName":"Roosevelt",
			"jobTitle": "26th President of the United States"
		}
	}
]

ic.bulk_update_user(users=presidents)
```
