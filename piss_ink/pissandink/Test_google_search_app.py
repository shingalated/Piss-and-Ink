#!/usr/bin/env python
# Google search CLI

import urllib
import json
import sys
import textwrap
import getopt
import re

content_wrapper = textwrap.TextWrapper(initial_indent=" * ", \
    subsequent_indent="   ", width=80)

def usage():
    print "Usage: %s [-n results] [-s start] searchterm1 [searchterm2 ...]" % \
        sys.argv[0]
    sys.exit(1)

def process_content(content):
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'( )+', ' ', content)
    content = content.replace("&#39;","'")
    content = content.replace("&quot;",'"')
    return content_wrapper.fill(content)

def main():
    opts, args = getopt.getopt(sys.argv[1:], "hn:s:", ["help", "number=", \
        "start="])
    number = 4
    start = 0
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-n", "--number"):
            if int(a) > 0:
                number = int(a)
        elif o in ("-s", "--start"):
            if int(a) > 0:
                start = int(a)
                
    if len(args) == 0:
        usage()
    
    search = '"%s"' % '" "'.join(args)
    while number > 0:
        query_dict = {'q' : search, 'rsz' : min(number, 8), 'start' : start}
        query = urllib.urlencode(query_dict)
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' \
            % (query)
        search_results = urllib.urlopen(url)
        results_json = json.loads(search_results.read())
        results = results_json['responseData']['results']
        for result in results:
            print "%s (%s):" %(result['titleNoFormatting'], \
                result['unescapedUrl'])
            print "%s\n" % process_content(result['content'])
        number -= 8
        start += 9

if __name__ == "__main__":
    main()
