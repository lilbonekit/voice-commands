from .browser import open_url


ENGLISH_VIDEO_URL = "https://youtu.be/scJciUkC-F4?si=cS24t1RQkSl4pOHx&t=14"
SPIDER_MAN_VIDEO_URL = "https://www.youtube.com/watch?v=OBpXq0XVyCw"
VNATURE_VIDEO_URL = "https://www.youtube.com/watch?v=zz9euLMWsfA&list=RDzz9euLMWsfA&start_radio=1"
# TODO: Replace with actual Supernatural URL
SUPERNATURAL_VIDEO_URL = SPIDER_MAN_VIDEO_URL

def open_english():
    open_url(ENGLISH_VIDEO_URL)

def open_spiderman():
    open_url(SPIDER_MAN_VIDEO_URL)

def open_vnature():
    open_url(VNATURE_VIDEO_URL)

def open_supernatural():
    open_url(SUPERNATURAL_VIDEO_URL)
