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


def reverse(words):
  r = {}
  for i,w in enumerate(words):
    r[w[0]] = r[w[1]] = i
  return r
  
def checker(words):
  r = {}
  for w in words:
    r[w[0]] = 0
    r[w[1]] = 1
  return r

WORDS = [s.strip().split() for s in open(DICT).read().strip().split("\n")]
REV = reverse(WORDS)
CHECK = checker(WORDS)

def check(s):
  return all(w in CHECK for w in s) and all(CHECK[w] == i % 2 for i,w in enumerate(s))

def read(decode, format, s):
  if decode:
    if not check(s):
      raise ValueError("Invalid word code.")
    return [REV[w] for w in s.split()]
  elif format=='ip4':
    return list(map(int, s.split('.')))
  elif format=='ip6':
    y = [int(x, 16) if x else 0 for x in s.split(':')]
    z = []
    for x in y:
      z.append(x // 256)
      z.append(x % 256)
    return z
  elif format=='mac':
    return [int(x, 16) for x in s.split(':')]
  else:
    return [int(s[i:i+2],16) for i in range(0,len(s),2)]
    

def write(decode, format, num):
  if not decode:
    return ' '.join(WORDS[i] for i in num)
  elif format == 'ip4':
    return '.'.join(num)
  elif format == 'ip6':
    num = [num[i] * 256 + num[i+1] for i in range(0,len(num),2)]
    return ':'.join(('000'+hex(i)[2:])[-4:] for i in num)
  elif format == 'mac':
    return ':'.join(('0'+hex(i)[2:])[-2:] for i in num)
  else:
    return ''.join(('0'+hex(i)[2:])[-2:] for i in num)
      

def arg():
  parser = argparse.ArgumentParser(
      prog='byteword', usage='%(prog)s [options]', 
      description='''Encode bytes as English words.
  '''
      )
  parser.add_argument(
      '-f, --format', type=str, 
      help='Which format to use', dest='format', metavar='ip4|ip6|mac'
      )
  parser.add_argument(
      '-d, --decode', action='store_const', 
      help='Decode given words', dest='decode', const=True, default=False
      )
  parser.add_argument(
      '-m, --multiple', action='store_const',
      help='Read multiple strings from stdin', dest='multiple', const=True, default=False
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
  elif args.multiple:
    strings = []
    try:
      while True:
        strings.append(input().strip())
    except EOFError:
      pass
  else:
    strings = [input().strip()]
  for s in strings:
    data = read(args.decode, args.format, s)
    print(write(args.decode, args.format, data))


main()
