import logging
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def is_valid(url):
    """
    Function returns True or False based on whether the url has to be fetched or not. This is a great place to
    filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
    in this method

    where we got trap detection help: https://support.archive-it.org/hc/en-us/articles/208332943-Identify-and-avoid-crawler-traps-

    """
    # ext = tldextract.extract(url)
    # print("subdomain: " + ext.subdomain, "domain: " +
    #       ext.domain, "suffix: " + ext.suffix)

    # parsed = urlparse(url)
    
    # if parsed.scheme not in set(["http", "https"]):
    #     return False

    url = "http://" + url
    parsed = urlparse(url)
    #print(parsed)
    try:
        url_path = parsed.path.lower()
        if ".ics.uci.edu" not in parsed.hostname or parsed.fragment != "" or re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" + "|thmx|mso|arff|rtf|jar|csv" + "|sql|java|prefs|class|h|cc|cpp|svn" + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", url_path) or ("grape" in parsed.hostname and (re.match("^.*attachment.*$", parsed.path) or re.match("^.*timeline.*$", url_path) or re.match("^.*action=diff.*$", parsed.query))) or re.match("^.*img.*$", url_path):
            # removed |txt|htm|
            # self.trap_links_file.write(url + "\n")
            ##print("BAD FILE TYPE")
            return False

        elif re.match("^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", url_path) or ("calendar" not in parsed.hostname and re.match("^.*calendar.*$", url_path)):
            # self.trap_links_file.write(url + "\n")
            ##print("REPEATING SUB-DIRECTORY")
            return False

        elif len(url_path) > 285:
            ##print("URL TOO LONG")
            return False

        else:
            return True

    except TypeError:
        print("TypeError for ", parsed)
        return False
