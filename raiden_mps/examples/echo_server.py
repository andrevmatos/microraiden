"""
This is dummy code showing how the minimal app could look like.
In his case we don't use a proxy, but directly a server
"""
from raiden_mps.proxy.paywalled_proxy import PaywalledProxy
from raiden_mps.config import CHANNEL_MANAGER_ADDRESS
import os
from raiden_mps.proxy.content import (
    PaywalledContent
)

if __name__ == '__main__':
    private_key = 'b6b2c38265a298a5dd24aced04a4879e36b5cc1a4000f61279e188712656e946'
    tempfile = os.path.join(os.path.expanduser('~'), '.raiden/echo_server.pkl')
    # set up a paywalled proxy
    # arguments are:
    #  - channel manager contract
    #  - private key to use for receiving funds
    #  - temporary file for storing state information (balance proofs)
    app = PaywalledProxy(CHANNEL_MANAGER_ADDRESS,
                         private_key,
                         tempfile)

    # add resource defined by regex and with a fixed price of 1 token
    #  third argument is an expression that will return actual content
    app.add_content(PaywalledContent(
                    "echofix\/[0-9]+", 1, lambda request:
                    (int(request.split("/")[1]), 200)))
    # resource with a price based on second param
    app.add_content(PaywalledContent(
                    "echodyn\/[0-9]+",
                    lambda request: int(request.split("/")[1]),
                    lambda request: (int(request.split("/")[1]), 200)))
    # start the app. proxy is a WSGI greenlet, so you must join it properly
    app.run(debug=True)
    app.join()
