#encoding=utf8
import urllib2
import urllib
import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#reg for get preorpost blog info
re_str = r'cb_blogId=(.*),cb_entryId=(.*),cb_blogApp.*cb_entryCreatedDate=\'(.*)\''
re_pat = re.compile(re_str)

#sample url for one blog in cnblogs
seedUrl = 'http://www.cnblogs.com/yuxc/archive/2011/08/24/2152667.html'

#save blogs info in local file
f = open("blogsofyuxc.txt", "a")

#function to get blogs
def GetBlog(url,direction):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    req = urllib2.Request(url,headers=header)
    res = urllib2.urlopen(req).read()
    soup = BeautifulSoup.BeautifulSoup(res)

    #get and print url and page title
    titles = soup.findAll(id = 'cb_post_title_url')
    info = dict(titles[0].attrs)['href'] + '   ' + titles[0].string
    print info
    f.write(info +"\n")

    #parse and get pre/post page info to form urls
    scripts = soup.findAll('script')
    blogId = 0
    entryId = 0
    CreateDate = ''

    for script in scripts:
        if(len(script.contents) >0):
            content = script.contents[0]
            if(content.find('allowComments') != -1):
                #print content
                search_re = re_pat.search(content)
                if search_re:
                    blogId = search_re.group(1)
                    entryId = search_re.group(2)
                    CreateDate = search_re.group(3)
                    break

    #get page for prevnext pages
    preposturl = r'http://www.cnblogs.com/post/prevnext?postId='+ entryId + r'&blogId='+ blogId +r'&dateCreated=' + CreateDate

    res1 = urllib.urlopen(preposturl).read()
    soup1 = BeautifulSoup.BeautifulSoup(res1)
    links = soup1.findAll('a')

    if(len(links)/2 > 1):
        if(direction == 0):
            linkl = links[1]
            linkr = links[3]
            GetBlogHistory(dict(linkl.attrs)['href'], -1)
            GetBlogHistory(dict(linkr.attrs)['href'], 1)
        elif(direction == -1):
            targetLink = links[1]
            GetBlogHistory(dict(targetLink.attrs)['href'], -1)
        else:
            targetLink = links[3]
            GetBlog(dict(targetLink.attrs)['href'], 1)
    else:
        if(direction == 0):
            targetLink = links[1]
            #todo, handle case if the page happened to be first or last one

GetBlogHistory(seedUrl, 0)