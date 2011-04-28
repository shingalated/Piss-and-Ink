import sys
import os
import xmpp

if len(sys.argv) < 3:
    print "Syntax: register.py [JID] [Password]"
    sys.exit(64)

jid=xmpp.protocol.JID(sys.argv[1])
cli=xmpp.Client(jid.getDomain(), debug=[])
cli.connect()

# getRegInfo has a bug that puts the username as a direct child of the
# IQ, instead of inside the query element.  The below will work, but
# won't return an error when the user is known, however the register
# call will return the error.
xmpp.features.getRegInfo(cli,
                         jid.getDomain(),
                         #{'username':jid.getNode()},
                         sync=True)

if xmpp.features.register(cli,
                          jid.getDomain(),
                          {'username':jid.getNode(),
                           'password':sys.argv[2]}):
    sys.stderr.write("Success!\n")
    sys.exit(0)
else:
    sys.stderr.write("Error!\n")
    sys.exit(1)
