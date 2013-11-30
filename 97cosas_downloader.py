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
import os, sys
from pyPdf import PdfFileWriter, PdfFileReader
import lxml.html, lxml.cssselect
from time import sleep
from urlparse import urljoin
import urllib2
from xhtml2pdf import pisa             # import python module


output_pdf_path = "/home/ocioz/Escritorio/97 cosas que todo programador.pdf"    # set your ouput path for file
url_base = 'http://97cosas.com/programador/'    # url where each chapter will be
temp_path = "/home/ocioz/Escritorio/temp"    # set temp path. If not exists, script create automatically


# Utility function
def convertHtmlToPdf(sourceHtml, output_pdfFilename):
    # open output_pdf file for writing (truncated binary)
    resultFile = open(output_pdfFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output_pdf file
    resultFile.close()                 # close output_pdf file

    # return True on success and False on errors
    return pisaStatus.err




def concatenate_pdf(book_title, num_chapters):
        fileList = os.listdir(temp_path)
        
        
        print"Uniendo pdfs..."
        output_pdf = PdfFileWriter()

        for i in range (1,num_chapters):
            f=open(temp_path+"/"+str(i)+"x97.pdf", "rb")
            num_pages=PdfFileReader(f).getNumPages()
            if num_pages==0:
                pdfOne = PdfFileReader(f).getPage(0)
                output_pdf.addPage(pdfOne)
            else:
                for a in range (0,num_pages):
                    pdfOne = PdfFileReader(f).getPage(a)
                    output_pdf.addPage(pdfOne)

        print file
        output_pdfStream = file(r""+book_title, "wb")
        output_pdf.write(output_pdfStream)
        output_pdfStream.close()
        print "Union finalizada\nTienes el archivo creado en..."+output_pdf_path
        for i in range(1,num_chapters+1):
            print "borrando... capitulo: "+str(i)
            os.remove(temp_path+"/"+str(i)+"x97.pdf")



def get_page_html(url):
    "return HtmlElement of url"
    request = requests.get(url)
    source = request.content
    return lxml.html.fromstring(source)

"""
******************
HTML and CSS style
******************
"""

body_style="""
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-size: 14px;
line-height: 20px;
color: #333333;
"""
pre_style="""
display: block;
padding: 9.5px;
margin: 0 0 10px;
font-size: 13px;
line-height: 20px;
word-break: break-all;
word-wrap: break-word;
white-space: pre-wrap;
background-color: #f5f5f5;
background-color: #772953;
color:#FFFFFF;
border-radius: 4px;
"""
code_style="""
font-family: Monaco, Menlo, Consolas, "Courier New", monospace;
font-size: 12px;
font-weight:bold;
white-space:pre
"""

"""
*************************
end of HTML and CSS style
*************************
"""


init = raw_input("Press enter to start downloading from\nhttp://97cosas.com/programador/\n(ONLY TEST)If you want concatenate PDFs files, press 1 and enter(ONLY TEST)\n")

if init == "1":
    concatenate_pdf("97 cosas que todo programador", 97)
    break

if not os.path.exists(temp_path):
    os.makedirs(temp_path)



html = get_page_html(url_base)    # get html code
sourceHtml="<div style='font-size:12px'>"

j = 1
max_num_chapter = 0
for i in html.cssselect('div.span12')[0].cssselect('ol')[0].cssselect('li'):    # every chapter iterator
    try:
        chapter_url = urljoin(url_base, i.cssselect('a')[0].get('href'))
        chapter_title = str(j) +" - "+ i.cssselect('a')[0].text_content()    # chapter's title
        html2 = get_page_html(chapter_url)     # chapter's html

        for x in html2.cssselect('div.span12')[0]:    # paragrap iterator
            if not (x.cssselect('ul.dropdown-menu') or "Leer contr" in x.text_content()):    # Do not want these elements
        		sourceHtml = sourceHtml + lxml.html.tostring(x)    # Convert HtmlElement to string and add

        print "Chapter "+str(j)+" created -",chapter_url
        sleep(.2)

        " Edit html with correct styles to create pdf file "
        sourceHtml = sourceHtml.replace("<body", "<body style='"+body_style+"'")
        sourceHtml = sourceHtml.replace("<pre", "<pre style='"+pre_style+"'")
        sourceHtml = sourceHtml.replace("<code", "<code style='"+code_style+"'")
        sourceHtml = sourceHtml.replace("<h2", "<h2 style='font-size:31.5px'")
        sourceHtml = sourceHtml.replace("<small", "<small style='font-weight:normal;font-size:15px;color:#999999'")
        sourceHtml = sourceHtml+"</div></body></html>"

        output_pdfFilename = str(j)+"x97.pdf" # Temp pdf file
        j+=1
        pisa.showLogging()
        convertHtmlToPdf(sourceHtml, temp_path+"/"+output_pdfFilename)
        sourceHtml = ""    # Clear html text for another chapter

    except requests.exceptions.ConnectionError:
        print "Error de conexion",chapter_url,", "
        j+=1
    max_num_chapter += 1


sleep(5)
raw_input("Press enter to concatenate "+str(max_num_chapter)+" pdf files")

concatenate_pdf("97 cosas que todo programador", max_num_chapter)





























