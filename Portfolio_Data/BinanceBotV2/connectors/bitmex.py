import requests


def get_contracts():

    contracts = []

    response = requests.get("https://www.bitmex.com/api/v1/instrument/active")

    for contract in response.json():
        contracts.append(contract['symbol'])

    return contracts