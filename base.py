from __future__ import print_function
from urllib import urlopen
from lxml import html
from bs4 import BeautifulSoup
from pdb import set_trace

def ant_releases():
  con = urlopen("https://archive.apache.org/dist/ant/")
  dom = html.fromstring(con.read())
  for link in dom.xpath('//a/@href'):
    if 'RELEASE-NOTES' in link:
      note=urlopen("https://archive.apache.org/dist/ant/"+link).read()
      soup = BeautifulSoup(note)
      for script in soup(["script", "style"]):
          script.extract()    # rip it out

      # get text
      text = soup.get_text()

      # break into lines and remove leading and trailing space on each
      lines = (line.strip() for line in text.splitlines())
      # break multi-headlines into a line each
      chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
      # start=0
      # end=-1
      # for indx,chunk in enumerate(chunks):
      #   if "Fixed bugs" in chunk:
      #     start=indx
      #   if "Other changes" in chunk:
      #     end=indx
      # drop blank lines
      text = '\n'.join([c for c in chunks if c])
      with open(link[:-5]+'.txt', 'w') as file:
        file.write(text)

      # print(text)
      # set_trace()

      # print(link)


ant_releases()