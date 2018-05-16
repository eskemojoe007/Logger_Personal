# Logger
This repository is based on the `logging` package but adds some color functionality
as well as a format I find desirable.

You muse use `logger = customLogger('root')` to get the proper logger.  Keep in
mind that `'root'` can be any name you like, but root is generally the norm.

You can change the logging level by calling `logger.setLevel('INFO')`, default is
`'DEBUG'`.  You need to use all caps and a logging paramter (DEBUG,INFO,WARNING,ERROR,CRITICAL)

## Installation
There are many ways to install this repository.  You can clone and install locally, or just directly from Git.  It is not registered with pip just yet.  

#### Method 1 - Install using pipenv from git
```
pipenv install git+https://github.com/eskemojoe007/colored_logger#egg=colored_logger
```

#### Method 2 - Install using pipenv from cloned repo
Clone the repository to a local area then do
```
pipenv install -e <PATH TO FOLDER>
```

`<PATH TO OLDER>` could just be `..\colored_logger`

## OLD USAGE METHOD Usage
This is a complete package, but usage can be a little confusing:

```python
import sys
import os
# Put your path to these files here, where home is your default home
home = os.path.expanduser("~")
sys.path.append(os.path.join(home,'Documents','GitHub'))

from colored_logger.colored_logger import customLogger
logger = customLogger('root')
logger.setLevel('INFO')
```
