# Logger
This repository is based on the `logging` package but adds some color functionality
as well as a format I find desirable.

You muse use `logger = customLogger('root')` to get the proper logger.  Keep in
mind that `'root'` can be any name you like, but root is generally the norm.

You can change the logging level by calling `logger.setLevel('INFO')`, default is
`'DEBUG'`.  You need to use all caps and a logging paramter (DEBUG,INFO,WARNING,ERROR,CRITICAL)

## Usage
This is a complete package, but usage can be a little confusing:

```python
import sys
import os
# Put your path to these files here, where home is your default home
home = os.path.expanduser("~")
sys.path.append(os.path.join(home,'Documents','GitHub'))

from Logger import customLogger
logger = customLogger('root')
logger.setLevel('INFO')
```
