def record_user_click(index,keyword,url):
    urls = lookup(index,keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1] + 1

def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            for element in entry[1]:
                if element[0] == url:
                    return
            entry[1].append([url,0])
            return
    # not found, add new keyword to index
    index.append([keyword, [[url,0]]])

def get_page(url):
    import urllib
    url = urllib.urlopen(url)
    p =  url.read()
    return p

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed, max_depth):
    tocrawl = [seed]
    crawled = []
    index = []
    #pageNum = 0
    next_depth = []
    depth = 0
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        #if pageNum >= max_pages:
         #   break
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            union(next_depth, get_all_links(get_page(page)))
            crawled.append(page)
    if not tocrawl:
        tocrawl, next_depth = next_depth, []
        depth += 1
        #pageNum += 1
    return index

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return None




liveLinks = crawl_web('http://www.udacity.com/cs101x/index.html', 12)
for element in liveLinks: print element
