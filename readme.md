# Currencies Converter App

Currencies converter app created with Python and Flask (restful api).

## Demo app

Demo app is deployed on Heroku PaaS.

## Docker


## Usage

To check if the server is running on localhost port 80 (GET request).

```commandline
$ curl http://localhost/
{
    "server": "running",
    "app": "currency converter"
}
```

Get list of all currencies and rates (GET request).

```commandline
/rates
```

Parameters:
- none

```commandline
$ curl http://localhost/rates
{
    "success": "true",
    "timestamp": 1645964069,
    "base": "EUR",
    "date": "2022-02-27",
    "rates": {
        ...
        "BTC": 2.8869014e-05,
        "EUR": 1,
        "GBP": 0.841179,
        ...
    }
}
```

Convert money from one currency to the other (GET request).

```commandline
/convert/<from_money>/<from_currency>/<to_currency>
```

Parameters: 
- from_money (float)
- from_currency (string)
- to_currency (string)

```commandline
$ curl http://localhost/convert/1234/USD/GBP
{
    "success": "true",
    "result": {
        "USD": 1234,
        "GBP": 920.8276027865726
    }
}
```

Reset and update the rates (POST request).

`/rates/reset`

Parameters:
- none

```commandline
$ curl -X POST http://localhost:3333/rates/reset
{
    "success": "true",
    "timestamp": 1645965366,
    "base": "EUR",
    "date": "2022-02-27",
    "rates": {
        ...
    }
}
```

Add new currency and new rates to the rates list (POST request) .

`/rates`

Parameters:
- new_currency (string)
- new_rate (float)

```commandline
$ curl -X POST -F 'new_currency=icp' -F 'new_rate=1.22222' http://localhost:3333/rates
{
    "success": "true",
    "result": {
        "ICP": 1.22222,
        "rates": {
            ...
            "ICP": 1.22222
        }
    }
}
```

Update currency with a new rate (PUT request).

`/rates`

Parameters:
- currency (string)
- new_rate (float)

```commandline
$ curl -X PUT -F 'currency=icp' -F 'new_rate=1.29222' http://localhost/rates
{
    "success": "true",
    "result": {
        "ICP": 1.29222,
        "rates": {
            ...
            "ICP": 1.29222
        }
    }
}
```

Delete currency from the list (DELETE request).

`/rates`

Parameters:
- currency (string)

```commandline
$ curl -X DELETE -F 'currency=icp' http://localhost/rates
```

Good luck.