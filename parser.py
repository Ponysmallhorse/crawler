# def get_text(data):
#     handler = html2text.HTML2Text()
#     handler.ignore_links = True
#     handler.ignore_images = True
#     handler.ignore_emphasis = True
#     return handler.handle(data=data)
#
# def get_links(data):
#     handler = html2text.HTML2Text()
#     handler.ignore_images = True
#     handler.ignore_emphasis = True
#     handler.l
#
import urllib3.util

print('.'.join(urllib3.util.parse_url('https://www.nytimes.com').host.split('.')[-2:]))