import logging

logger = logging.getLogger('LOG')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('./log.log')
fh.setLevel(logging.DEBUG)  #

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  #

formatter = logging.Formatter('%(asctime)s->%(name)s->%(levelname)s=%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == '__main__':
    pass