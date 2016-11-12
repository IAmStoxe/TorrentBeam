from bs4 import BeautifulSoup
from urlparse import urljoin
import urllib2
import json
from search_result import SearchResult


def load_config():
    with open('./search_config.json') as f:
        return json.load(f)


def get_single_site_info(site_name):
    config = load_config()
    for item in config:
        if item['name'].lower() == site_name.lower():
            return item


def call_url(url):
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        html = response.read()
        return html


def torlock(search_term):
    config = get_single_site_info('TorLock')
    search_url = config['search_url'] % search_term
    html_doc = call_url(search_url)
    parsed_results = parse_document(html_doc, search_url, config)

    ret_arr = []
    for i in range(parsed_results['links'].__len__()):
        ret_arr.append(SearchResult(parsed_results['titles'][i].get_text(),
                                    parsed_results['links'][i],
                                    parsed_results['added'][i].get_text(),
                                    parsed_results['seeds'][i].get_text()))
    return ret_arr


def parse_document(html, search_url, config):
    soup = BeautifulSoup(html, 'html.parser')
    added_sel, link_sel, seeds_sel, title_sel = load_css_selectors(config)
    titles = soup.select(title_sel)
    rel_links = soup.select(link_sel)
    abs_links = get_absolute_urls(search_url, rel_links)
    added_date = soup.select(added_sel)
    seeds = soup.select(seeds_sel)
    return {
        "links": abs_links,
        "added": added_date,
        "seeds": seeds,
        "titles": titles
    }


def load_css_selectors(config):
    title_sel = config['results_css_selector']['title']
    link_sel = config['results_css_selector']['link']
    added_sel = config['results_css_selector']['added']
    seeds_sel = config['results_css_selector']['seeds']
    return added_sel, link_sel, seeds_sel, title_sel


def get_absolute_urls(search_url, rel_links):
    ret_arr = []
    for link in rel_links:
        ret_arr.append(urljoin(search_url, link['href']))
    return ret_arr


def main():
    for item in torlock('photoshop'):
        print item.toJSON()


main()
