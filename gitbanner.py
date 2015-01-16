#!/usr/bin/env python
#
# Fred C. <github-fred@hidzz.com>
#
import os
import subprocess
import sys
import yaml

from datetime import datetime, timedelta

BANNER_INFO_FILE = 'banner.yaml'
DATAFILE = 'commits.dat'
SUNDAY = 6

def build_banner_data(filename):
  try:
    with open('banner.yaml') as fdin:
      banner = yaml.load(fdin)
  except (IOError, yaml.YAMLError) as err:
    raise StandardError(err)

  # Check if all the fields are present.
  for field in ('start_date', 'message'):
    if field not in banner:
      raise StandardError('The field "%s" is missing' % field)

  try:
    start_date = datetime.strptime(banner['start_date'], '%m/%d/%Y')
    if start_date.weekday() != SUNDAY:
      raise ValueError('The date must start on a sunday')
  except ValueError as err:
    raise StandardError(err)

  message = banner['message'].splitlines()
  # Check for the number of lines and the length of all the lines.
  if len(message) != 7:
    raise StandardError('Only 7 lines are allowed (there is 7 days/week)')
  if not all([len(message[0]) == len(l) for l in message[1:]]):
    raise StandardError('All the lines must have the same length')

  # Build the data structure.
  commit = {}
  number_of_days = len(message[0]) * 7
  for day in range(number_of_days):
    date = start_date + timedelta(days=day)
    push = True if message[day % 7][day / len(message)] == '*' else False
    commit[date.date()] = push

  return commit


def main():
  commit_data = build_banner_data(BANNER_INFO_FILE)
  today = datetime.now().date()
  if today not in commit_data:
    print 'Nothing to commit for today: %s' % today
    sys.exit(os.EX_OK)

  with open(DATAFILE, 'a') as fdout:
    fdout.write("%s - %s" % today, commit_data[today])

  command = lambda cmd: subprocess.check_call(shlex.split(cmd))
  command('git commit -am "Last update: %s"' % today)
  command('git push origin')


if __name__ == '__main__':
  main()
