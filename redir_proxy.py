from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless

"""
This example shows two ways to redirect flows to other destinations.
https://github.com/mitmproxy/mitmproxy/blob/master/examples/redirect_requests.py
"""


def request(context, flow):
    # pretty_host(hostheader=True) takes the Host: header of the request into account,
    # which is useful in transparent mode where we usually only have the IP
    # otherwise.

    # Method 2: Redirect the request to a different server
    if flow.request.pretty_host(hostheader=True).endswith("facebook.com"):
        flow.request.host = "192.168.0.12"
        flow.request.update_host_header()
