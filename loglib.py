import logging, sys

def init_logging(report_file=None):
    logger = logging.getLogger('sync_ad_zimbra_stream')
    hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('{%(levelname)s} %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    logger = logging.getLogger('sync_ad_zimbra_report')
    if report_file:
        hdlr = logging.FileHandler(report_file)
    else:
        hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s]%(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)


def get_report_logger():
    return logging.getLogger('sync_ad_zimbra_report')

def get_stream_logger():
    return logging.getLogger('sync_ad_zimbra_stream')
