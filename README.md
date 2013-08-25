byteword
========

Render binary data as a sequence of English words using the [PGP word list](http://en.wikipedia.org/wiki/PGP_word_list).

help
----
```
usage: byteword [options]

Encode bytes as English words.

optional arguments:
  -h, --help            show this help message and exit
  -f, --format ip4|ip6|mac
                        Which format to use
  -d, --decode          Decode given words
  -m, --multiple        Read multiple strings from stdin
  -s, --string <string>
                        Accept string on commandline instead of stdin
```