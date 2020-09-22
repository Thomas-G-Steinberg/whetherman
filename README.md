# WHETHERMAN

*"I'm the Whether Man, not the Weather Man, for after all it's more important to know whether there will be weather than what the weather will be."* - *The Phantom Tollbooth*


A CLI Weather Forecast Reader. Uses the weather.gov official API.


## Installation


Clone the repo and run ```pip3 install .```


## Usage

```
whetherman [-h] [-C CONFIG] [-H] [-L L L] [-N N]

optional arguments:
  -h, --help            show this help message and exit
  -C CONFIG, --config CONFIG
                        Configuration file to use; defaults to
                        ~/.whetherman.conf
  -H, --hourly          Display hourly forecasts rather than AM/PM summaries
  -L L L, --set-location L L
                        set location based on latitude/longitude
  -N N, --set-number N  number of entries displayed
```


