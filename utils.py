import logging

debug_mode = True


def create_logger(logger_name):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app_log.log',
        filemode='a'
        )

    return logging.getLogger(logger_name)


def print_and_log(msg, header=False, logger=create_logger('weather_app')):
    if header:
        pass
    else:
        msg = '     ' + msg
    
    logger.info(msg)
    if debug_mode:
        print(_format_line(msg, header))


def _format_line(msg, header=True):
    """Adds a format line after each message."""
    if header:
        format_line = '-----==========-----'
    else:
        format_line = '     -----==========-----'

    return msg + '\n' + format_line


def deco_print_and_log(msg):
    """Logs message and if debug mode is enabled, prints to console."""
    def inner_deco(func):
        def wrapper(*args):
            msg_lst = [' - Begin', ' - End']

            print_and_log(msg  + msg_lst[0], True)

            result = func(*args)

            print_and_log(msg  + msg_lst[1], True)

            return result
        return wrapper
    return inner_deco
