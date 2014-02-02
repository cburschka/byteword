#!/usr/bin/env python3

import byteword
import argparse

def read(decode, format, s):
  if decode:
    try:
      x = byteword.decode(s.split())
    except:
      x = byteword.decode(['aardvark'] + s.split())[1:]
    return x
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
    

def write(decode, format, bytes):
  if not decode:
    return ' '.join(byteword.encode(bytes))
  elif format == 'ip4':
    return '.'.join(bytes)
  elif format == 'ip6':
    bytes = [bytes[i] * 256 + bytes[i+1] for i in range(0,len(bytes),2)]
    return ':'.join(('000'+hex(i)[2:])[-4:] for i in bytes)
  elif format == 'mac':
    return ':'.join(('0'+hex(i)[2:])[-2:] for i in bytes)
  else:
    return ''.join(('0'+hex(i)[2:])[-2:] for i in bytes)
      

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
      help='Accept string on commandline instead of stdin', metavar='<string>', dest='string'
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
