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
import os

DICT=os.path.dirname(os.path.realpath(__file__)) + '/words.txt'


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

WORDS = [s.strip().split() for s in open(DICT).read().lower().strip().split("\n")]
REV = reverse(WORDS)
CHECK = checker(WORDS)

def check(words):
  return all(w in CHECK for w in words) and all(CHECK[w] == i % 2 for i,w in enumerate(words))

def decode(words):
  assert check(words)
  x = bytes([REV[w] for w in words])
  return x

def encode(data):
  return [WORDS[m][i%2] for i,m in enumerate(data)]
