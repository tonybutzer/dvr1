#!/usr/bin/env python
"""zap2xml.py -- The simplest zap2it scraper I could write.

Around June 2020 the `zap2xml.pl` I had stopped working.  It generated HTTP
requests that gave only 400 responses.  I tried to patch it, to the point that
it got OK responses, but parsed no data from them.  The zap2it site must have
changed.  I thought they had an API, but apparently this tool has always
scraped the internal JSON feed, intended just for the web site?

So re-write from scratch.  Simplest possible form I can, so the fewest things
need to change if the site ever does again.  The goal is to feed guide data
into Tvheadend.

The zap2it site, at least for my area/OTA, will give "400 Bad Request" errors
*for certain times* of certain days.  Even their own site does this!  This is
the error that recently started tripping up `zap2xml.pl`.  So this tool simply
ignores 400 errors, continuing to gather the data available for other time
windows.

Written to have only standard library dependencies.
"""

import argparse
import datetime
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def get_args():
  parser = argparse.ArgumentParser(
      description='Fetch TV data from zap2it.',
      epilog='This tool is noisy to stdout; '
          'with cron use chronic from moreutils.')
  parser.add_argument(
      '--aid', dest='zap_aid', type=str, default='gapzap',
      help='Raw zap2it input parameter.  (Affiliate ID?)')
  parser.add_argument(
      '-c', '--country', dest='zap_country', type=str, default='USA',
      help='Country identifying the listings to fetch.')
  parser.add_argument(
      '-d', '--delay', dest='delay', type=int, default=5,
      help='Delay, in seconds, between server fetches.')
  parser.add_argument(
      '--device', dest='zap_device', type=str, default='-',
      help='Raw zap2it input parameter.  (?)')
  parser.add_argument(
      '--headend-id', dest='zap_headendId', type=str, default='lineupId',
      help='Raw zap2it input parameter.  (?)')
  parser.add_argument(
      '--is-override', dest='zap_isOverride', type=bool, default=True,
      help='Raw zap2it input parameter.  (?)')
  parser.add_argument(
      '--language', dest='zap_languagecode', type=str, default='en',
      help='Raw zap2it input parameter.  (Language.)')
  parser.add_argument(
      '--pref', dest='zap_pref', type=str, default='',
      help='Raw zap2it input parameter.  (Preferences?)')
  parser.add_argument(
      '--timespan', dest='zap_timespan', type=int, default=3,
      help='Raw zap2it input parameter.  (Hours of data per fetch?)')
  parser.add_argument(
      '--timezone', dest='zap_timezone', type=str, default='',
      help='Raw zap2it input parameter.  (Time zone?)')
  parser.add_argument(
      '--user-id', dest='zap_userId', type=str, default='-',
      help='Raw zap2it input parameter.  (?)')
  parser.add_argument(
      '-z', '--zip', '--postal', dest='zap_postalCode', type=str, required=True,
      help='The zip/postal code identifying the listings to fetch.')
  return parser.parse_args()


def main():
  args = get_args()
  print(type(args))
  base_qs = {k[4:]: v for (k, v) in vars(args).items() if k.startswith('zap_')}
  done_channels = False
  err = 0
  print(base_qs)
  sys.exit(err)


if __name__ == '__main__':
  main()
