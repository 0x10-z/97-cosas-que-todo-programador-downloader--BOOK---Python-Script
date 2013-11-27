#!usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Iker Ocio Zuazo
# Mail Contact: ikerocio@gmail.com
# Web: http://ikerocio.com

# Acknowledgement to Espartaco Palma (@esparta) and Natán Calzolari for translate into Spanish. Original book http://programmer.97things.oreilly.com/wiki/index.php/97_Things_Every_Programmer_Should_Know
# This code have a Creative Commons Attribution 3 license - http://creativecommons.org/licenses/by/3.0/es/
# You can: 
# Share — copy and redistribute the material in any medium or format 
# and
# Adapt — remix, transform, and build upon the material
#

import requests
import lxml.html, lxml.cssselect
import time
from urlparse import urljoin
import urllib2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak

#init = raw_input("Press enter to start downloading from\nhttp://97cosas.com/programador/")

output = "/home/ocioz/Escritorio/97 cosas que todo programador.pdf"    # set your ouput path for file
url_base = 'http://97cosas.com/programador/'    # url where every chapter is
request = requests.get(url_base)                # 
source = request.content    # get request source
html = lxml.html.fromstring(source)    # get html code


j = 1

# PDF STYLESHEET
style_sheet=getSampleStyleSheet()    # pdf style sheet
style_sheet.fontSize=50    # this doesn't work
story=[]    # story object where we are going to save every chapter for then export to pdf
h1 = style_sheet['Heading1']    
style=style_sheet['BodyText']

for i in html.cssselect('div.span12')[0].cssselect('ol')[0].cssselect('li'):    # every chapter iterator
    
    chapter_url = urljoin(url_base, i.cssselect('a')[0].get('href'))    # chapter's url
    chapter_title = str(j) +" - "+ i.cssselect('a')[0].text_content()    # chapter's title
    

    chapter_content = requests.get(chapter_url).content    
    html2 = lxml.html.fromstring(chapter_content)     # chapter's html
    chapter_author = html2.cssselect('div.span12')[0].cssselect('small')[0].text_content() # chapter's real author

    # put chapter title into pdf
    h1.pageBreakBefore=0      # 0 page break
    h1.keepWithNext=1
    p1 = Paragraph(chapter_title, h1)
    story.append(p1)
    story.append(Spacer(0,15)) # title and body spacer
   
    for x in html2.cssselect('div.span12')[0].cssselect('p'):    # paragrap iterator
        if not "Leer contr" in x.text_content():
            # print x.text_content()
            p2=Paragraph(x.text_content(),style)    # set paragraph into storyboard
            story.append(p2)    # set storyboard into pdf
            time.sleep(.5)
            

    print "Chapter "+str(j)+" created"
    j+=1
    story.append(PageBreak())    

pdf=SimpleDocTemplate(output,pagesize=A4,showBoundary=1)    # create a pdf template
pdf.build(story)


