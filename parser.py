#!/usr/bin/python
# coding=utf8

from collections import OrderedDict
from datetime import datetime
from os.path import basename
import os
import sys

''' init dictionary with Name/Checkin/CheckinAbnormal attributes '''
def initDict():
  with open('raw_data/staffInformation.txt') as openfileobject:
    for line in openfileobject:
      records = line.split(',')
      record[records[2].strip()] = {'CName': records[0].strip(),
                                    'EName': records[1].strip(),
                                    'Checkin': 'Absent',
                                    'CheckinAbnormal': False}

def processCheckin(fileName):
  with open(fileName) as openfileobject :
    for line in openfileobject:

      tmp = line.split(',')
      idInfo = tmp[-1].split(':')
      if len(idInfo) >2:
        id = idInfo[2].strip()
        time = tmp[0]

        try:
          value = record[id]
          if value['Checkin'] == 'Absent':
            value['Checkin'] = time
          elif value['Checkin'] > time:
            value['Checkin'] = time
        except KeyError:
          # Key is not present
          pass

def processAbnormal():
  for key, value in record.iteritems() :
    if record[key]['Checkin'] == 'Absent':
      record[key]['CheckinAbnormal'] = True
    elif record[key]['Checkin'].split(' ')[1] > '10:00:00':
      record[key]['CheckinAbnormal'] = True

def writeParsedRecord(fileName):
  f = 'result/' + os.path.splitext(fileName)[0].split('/')[-1] + '_result.txt'
  print f
  if not os.path.exists(os.path.dirname(f)):
    try:
        os.makedirs(os.path.dirname(f))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
  fileToWrite = open(f, 'w+')
  for key, value in record.iteritems() :
    fileToWrite.write('{0}, {1}, {2}\n'.format(record[key]['CName'], record[key]['Checkin'], record[key]['CheckinAbnormal']))
  fileToWrite.close()

if len(sys.argv) <=1:
  sys.stderr.write('Usage: python parser.py <fileName>')
  sys.exit(1)

fileName = sys.argv[1]
record = OrderedDict()
initDict()
processCheckin(fileName)
processAbnormal()
writeParsedRecord(fileName)

