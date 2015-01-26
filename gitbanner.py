#!/usr/bin/env python
#
# Fred C. <github-fred@hidzz.com>
#
import os
import shlex
import subprocess
import sys
import tempfile
import yaml

from datetime import datetime

BANNER_INFO_FILE = 'banner.yaml'
DATAFILE = 'commits.dat'
SUNDAY = 6
HEADER = """#
# This file will be changed just to have something to commit.
# Last update: %s
#
"""

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

  message = banner['message'].splitlines()
  # Check for the number of lines and the length of all the lines.
  if len(message) != 7:
    raise StandardError('Only 7 lines are allowed (there is 7 days/week)')
  if not all([len(message[0]) == len(l) for l in message[1:]]):
    raise StandardError('All the lines must have the same length')

  # Is today a push day?
  if today < start_date:
    raise StandardError('Today is before start date')

  number_of_days = len(message) * len(message[0])
  day = (today - start_date).days
  try:
    push = True if message[day % 7][day / len(message)] == '#' else False
  except IndexError:
    raise StandardError('The banner is fully printed')

  return (push, day, number_of_days)


def main():
  try:
    push, day, days_left = is_pushday(BANNER_INFO_FILE)
  except StandardError as err:
    print err
    sys.exit(os.EX_OSERR)

  msg = "Push: %s, Day: %s, Days left: %s" % (push, day, days_left - day)
  try:
    with tempfile.TemporaryFile() as fdtmp:
      fdtmp.write(HEADER % datetime.now())
      fdtmp.write(msg)
      fdtmp.write('\n')
      # copy the content of the old DATAFILE into the tmpfile.
      with open(DATAFILE, 'r') as fdin:
        for line in fdin:
          if line.startswith('#'):
            continue
          fdtmp.write(line)

      # copy the content of the tmpfile into the new datafile.
      fdtmp.seek(0)
      with open(DATAFILE, 'w') as fdout:
        for line in fdtmp:
          fdout.write(line)

  except IOError as err:
    print err
  else:
    # send everything to github.com if it's a 'commit' day.
    if push:
      command = lambda cmd: subprocess.check_call(shlex.split(cmd))
      command('git commit -am "%s"' % msg )
      command('git push origin')


if __name__ == '__main__':
  main()
