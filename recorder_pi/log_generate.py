#!/bin/python3
import logging


if __name__ == "__main__":
    logging.critical('Hwloooo')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %a %H:%M:%S',
                        filename='../log/test.log',
                        filemode='w')

    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')