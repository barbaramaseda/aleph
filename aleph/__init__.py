import os
import logging
from sqlalchemy.exc import SAWarning

# shut up useless SA warning:
import warnings
warnings.filterwarnings('ignore',
                        'Unicode type received non-unicode bind param value.')

warnings.filterwarnings('ignore', category=SAWarning)

# loggers.
logging.basicConfig(level=logging.DEBUG)

# specific loggers
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('pyelasticsearch').setLevel(logging.WARNING)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('boto').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('amqp').setLevel(logging.INFO)

# default locale settings
os.environ['LC_ALL'] = 'en_US'
os.environ['LC_LANG'] = 'en_US'
os.environ['LC_CTYPE'] = 'en_US'
os.environ['LANG'] = 'en_US'
