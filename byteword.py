#!/usr/bin/python3

# Copyright 2013 Christoph Burschka <christoph@burschka.de>

#  This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse

DICT='words.txt'

def read_dict(txt):
  return open(txt).read().strip().split()

def reverse(words):
  r = {}
  for i,w in enumerate(words):
    r[w] = i
    
  return r

WORDS = list(read_dict(DICT))
REV = reverse(WORDS)

def read(decode, ip4, s):
  if decode:
    return [REV[w] for w in s.split()]
  elif ip4:
    return list(map(int, s.split('.')))
  else:
    return [int(s[i:i+2],16) for i in range(0,len(s),2)]
    

def write(decode, ip4, num):
  if not decode:
    return ' '.join(WORDS[i] for i in num)
  elif ip4:
    return '.'.join(num)
  else:
    return ''.join(('0'+hex(i)[2:])[-2:] for i in num)
      

def arg():
  parser = argparse.ArgumentParser(
      prog='byteword', usage='%(prog)s [options]', 
      description='''Encode bytes as English words.
  '''
      )
  parser.add_argument(
      '-i, --ip4', action='store_const', 
      help='Use IPv4 dotted decimal format', dest='ip4', const=True, default=False
      )
  parser.add_argument(
      '-d, --decode', action='store_const', 
      help='Decode given words', dest='decode', const=True, default=False
      )
  parser.add_argument(
      '-s, --string', type=str, 
      help='Accept string on commandline instead of stdin', metavar='L', dest='string'
      )
  return parser

def main():
  args = arg().parse_args()
  
  if args.string:
    strings = [args.string]
  else:
    strings = []
    try:
      while True:
        strings.append(input().strip())
    except EOFError:
      pass

  for s in strings:
    data = read(args.decode, args.ip4, s)
    print(write(args.decode, args.ip4, data))


main()
