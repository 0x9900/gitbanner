#!/usr/bin/env python
#
# Fred C. <github-fred@hidzz.com>
#
import os
import shlex
import subprocess
import sys
import yaml

from datetime import datetime

BANNER_INFO_FILE = 'banner.yaml'
DATAFILE = 'commits.dat'
SUNDAY = 6

def is_pushday(filename, today=datetime.now().date()):

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
    start_date = start_date.date()
    if start_date.weekday() != SUNDAY:
      raise ValueError('The date must start on a sunday')
  except ValueError as err:
    raise StandardError(err)

  if today < start_date:
    raise StandardError('Today is before start date')

  message = banner['message'].splitlines()
  # Check for the number of lines and the length of all the lines.
  if len(message) != 7:
    raise StandardError('Only 7 lines are allowed (there is 7 days/week)')
  if not all([len(message[0]) == len(l) for l in message[1:]]):
    raise StandardError('All the lines must have the same length')

  # Is today a push day?
  number_of_days = len(message) * len(message[0])
  day = (today - start_date).days
  try:
    push = True if message[day % 7][day / len(message)] == '*' else False
  except IndexError:
    raise StandardError('The banner is fully printed')

  return (push, day, number_of_days)


def main():
  try:
    push, day, days_left = is_pushday(BANNER_INFO_FILE)
  except StandardError as err:
    print err
    sys.exit(os.EX_OSERR)

  msg = "Push: %s, Day: %s, Days left: %s" % (push, day, days_left)
  try:
    with open(DATAFILE, 'a') as fdout:
      fdout.write(msg)
      fdout.write('\n')
  except IOError as err:
    print err
  else:
    if push:
      command = lambda cmd: subprocess.check_call(shlex.split(cmd))
      command('git commit -am "%s"' % msg )
      command('git push origin')


if __name__ == '__main__':
  main()
