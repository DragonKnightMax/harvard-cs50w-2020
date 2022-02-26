airports = [
    {
        "name": "Beijing Capital International Airport",
        "code": "PEK",
        "country": "China"
    },
    {
        "name": "Los Angeles International Airport",
        "code": "LAX",
        "country": "United States"
    },
    {
        "name": "London Heathrow Airport",
        "code": "LHR",
        "country": "United Kingdom"
    }
]

for airport in airports:
    print(f"{airport['name']} ({airport['code']}) is in {airport['country']}.")
