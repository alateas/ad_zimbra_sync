import logging

def init_logging(report_file=None):
    logger = logging.getLogger('sync_ad_zimbra_stream')
    hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    logger = logging.getLogger('sync_ad_zimbra_report')
    if report_file:
        hdlr = logging.FileHandler(report_file)
    else:
        hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)


def get_report_logger():
    return logging.getLogger('sync_ad_zimbra_report')

def get_stream_logger():
    return logging.getLogger('sync_ad_zimbra_stream')
