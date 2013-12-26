#!/usr/bin/env python3
import byteword, datetime, argparse

def b(n, d=4):
    x = []
    while n > 0:
        x.append(n & 0xff)
        n >>= 8
    x = x[::-1]
    if len(x) < d:
        x = ([0,0,0,0]+x)[-d:]
    return x

def bn(b):
    x = 0
    for i in b:
        x = (x << 8) | i
    return x

def arg():
  parser = argparse.ArgumentParser(
      prog='bytetime', usage='%(prog)s [options]', 
      description='''Encode timestamp as English words. Without arguments, the current time is encoded.
  '''
      )
  parser.add_argument(
      '-d, --decode', type=str, 
      help='Decode given words', dest='decode', metavar='L'
      )
  parser.add_argument(
      '-e, --encode', type=str, 
      help='Encode a given date-time (YYYY-MM-DD HH:MM:SS)', metavar='L', dest='encode'
      )
  return parser

def main():
  FORMAT = '%Y-%m-%d %H:%M:%S'
  args = arg().parse_args()
  if args.decode:
    z = bn(byteword.decode(args.decode.split()))
    y = z
    while z < 256**3:
        z <<= 8
        y = (y << 8) | 0xff
    print(datetime.datetime.fromtimestamp(z).strftime(FORMAT))
    if y != z:
        print(datetime.datetime.fromtimestamp(y).strftime(FORMAT))        
  else:
    x = datetime.datetime.strptime(args.encode, FORMAT) if args.encode else datetime.datetime.now()
    assert x.timestamp() >= 0
    print('Scaled:  ', ' '.join(byteword.encode(
        b(int(x.timestamp()/86400*65536))
    )))
    print('Unscaled:',' '.join(byteword.encode(b(int(x.timestamp())))))
    n = x.timestamp() // 65536 * 65536
    print('Current cycle: ',' '.join(byteword.encode(b(int(n//65536),2))),', ',datetime.datetime.fromtimestamp(n).strftime(FORMAT),' - ',datetime.datetime.fromtimestamp(n+65536).strftime(FORMAT))
    print('Next cycle will be:', ' '.join(byteword.encode(b(int(n//65536+1),2))))
    print('Current season: ',byteword.encode([int(n//2**24)])[0],', ',datetime.datetime.fromtimestamp(n//2**24*2**24).strftime(FORMAT),' - ',datetime.datetime.fromtimestamp(((n//2**24)+1)*2**24).strftime(FORMAT))
    print('Next season will be:', byteword.encode([int(n//2**24+1)])[0])
 
main()

