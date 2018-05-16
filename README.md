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

`<PATH TO FOLDER>` could just be `..\colored_logger`

#### OLD USAGE METHOD Usage
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

## Usage
Basic usage is very similar to any logging application:
```
from colored_logger import customLogger
logger = customLogger('root')

logger.info('This is an info message')
```

### Advanced Spacing
The logger, splits terminal output in a couple of interesting ways.

#### Line wrap
It will automatically wrap lines around leaving room for the flag of the logger level

```
from colored_logger import customLogger
logger = customLogger('root')

logger.debug('This is how line wrap works for very long lines, note that the '
    'width of the terminal is creating the length of the line wrap.')
```

![basic_wrap](https://user-images.githubusercontent.com/22135005/40120452-38dcc3f6-58ed-11e8-8897-dd812ebac5c2.png

#### Initial spacing
The initial space before the line will be preserved when wrapping

```
logger.debug('\tThis is how line wrap works for very long lines, note that the '
    'width of the terminal is creating the length of the line wrap.')
```
![tab_wrap](https://user-images.githubusercontent.com/22135005/40120485-4f278164-58ed-11e8-8656-e6b7c7bcb977.png

Spacing in the middle of lines is removed and replaced with spaces.

#### Manual line wraps
`\n` are still maintained throughout the message to control line breaks

```
logger.debug('\tThis is how line wrap works for very long lines,\nnote that the '
    'width of the terminal is creating the length of the line wrap.')
```

![line_wrap](https://user-images.githubusercontent.com/22135005/40120499-57bc22a8-58ed-11e8-8256-0dd94f530b93.png)
