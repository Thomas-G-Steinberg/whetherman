#!python3

import requests
from datetime import datetime, timezone
import json
import os.path
import sys
import textwrap
import argparse

SYMBOL_MAP = {
    'partly cloudy': '⛅',
    'cloudy': '☁️',
    'storm': '⛈',
    'sunny': '☀️',
    'rain': '🌧',
    'snow': '❄️'
}

API_ROOT = "https://api.weather.gov/"
DEFAULT_CONF = os.path.join(os.path.expanduser("~"), '.whetherman.conf')
def write_config(filename=DEFAULT_CONF, data=None):
    if data == None:
        data = {
            'wfo': '<FORECAST OFFICE HERE>',
            'xy': '<X COORD>,<YCOORD>',
            'units': 'us',
            'count': 1
        }
    with open(filename, "w") as json_file:
        json.dump(data, json_file)

def load_conf(filename=DEFAULT_CONF, exit_on_error=True):
    if os.path.exists(filename):
        if os.path.isfile(filename):
            with open(filename) as json_file:
                data = json.load(json_file)
                return data
        else:
            print("{} is a directory.".format(filename))
            sys.exit(1)
    else:
        write_config(filename)
        if exit_on_error:
            print("Stub config {} created - fill this file out and run again.".format(filename))
            sys.exit(1)
        else:
            return load_conf(filename,exit_on_error)


def endpoint(paths, args={}):
    argstr = ""
    for key in args:
        if argstr == "":
            argstr = "?"
        argstr += key + "=" + args[key]
    return API_ROOT + ("/".join(paths)) + argstr


def to_datetime(strrep):
    return datetime.strptime(strrep, "%Y-%m-%dT%H:%M:%S%z")


def parse_entry(entry, now=datetime.now(timezone.utc), hourly=False, force=False):
    start = to_datetime(entry['startTime'])
    end = to_datetime(entry['endTime'])
    shortcast = entry['shortForecast']
    symbol = ''
    for key in SYMBOL_MAP:
        if key in shortcast.lower():
            symbol = SYMBOL_MAP[key]
            break

    if force or (start <= now < end):
        time = start.strftime("%a %b %-d, %-I %p")
        cast = "{}  {}:".format(
            symbol,
            time
        ).strip()
        print(cast)
        if hourly:
            print("{} °{}, {}".format(
                entry['temperature'],
                entry['temperatureUnit'],
                shortcast
            ))
        else:
            casts = textwrap.wrap(entry['detailedForecast'])
            for line in casts:
                print(line)
        print()
        return True
    return False

def read_forecast(filename=DEFAULT_CONF, hourly=False):
    conf = load_conf(filename)
    wfo, xy = conf['wfo'], conf['xy']
    r = None
    args = {
        'units': conf['units']
    }
    try:
        path = ['gridpoints', wfo, xy, 'forecast']
        if hourly:
            path.append('hourly')
        uri = endpoint(path, args)
        r = requests.get(uri, timeout=5)
    except BaseException:
        print("Error: API timeout")
        return 1
    if r.status_code != 200:
        print("API error code", r.status_code)
        return 1
    res = r.json()
    periods = res['properties']['periods']
    now = datetime.now(timezone.utc)
    force = False
    count = conf['count']
    for period in periods:
        force = parse_entry(period, now, hourly, force)
        if force:
            count -= 1
        if count == 0:
            break
    return 0

def generate_config_from_gps(config, location):
    conf = load_conf(config,False)
    ll = ",".join(location)
    r = None
    try:
        uri = endpoint(['points', ll])
        r = requests.get(uri, timeout=5)
    except BaseException as e:
        print("Error: API timeout", e)
        return 1
    if r.status_code != 200:
        print("API error code", r.status_code)
        return 1
    res = r.json()
    props = res['properties']
    office = props['cwa']
    x = props['gridX']
    y = props['gridY']
    conf['xy'] = "{},{}".format(x,y)
    conf['wfo'] = office
    write_config(config,conf)

def set_config_result_num(config, num):
    conf = load_conf(config,False)
    conf['count'] = num
    write_config(config,conf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--config', default=DEFAULT_CONF)
    parser.add_argument('-H', '--hourly', action='store_true')
    parser.add_argument(
        '-L','--set-location', metavar='L', type=str, nargs=2,
        help='latitude/longitude', required=False
    )
    parser.add_argument(
        '-N','--set-number', metavar='N', type=int, nargs=1,
        help='number of entries displayed', required=False
    )
    args = parser.parse_args()
    if args.set_location != None:
        generate_config_from_gps(args.config, args.set_location)
    if args.set_number != None:
        set_config_result_num(args.config, args.set_number[0])
    return read_forecast(args.config,args.hourly)

if __name__ == "__main__":
    sys.exit(main())
