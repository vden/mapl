#-*- coding: utf-8 -*-
import re, os

f = open('chapter-02.tex','r+').readlines()
o = open('habr_conv', 'wr+')
s = '\n'.join(f)
s = unicode(s,'utf-8')
figure = r"""\documentclass[openany]{book}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{epigraph}
\usepackage{fancyvrb}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{url}
\usepackage[dvips]{color}
\usepackage[arrow,curve,matrix,frame]{xy}
\usepackage{array}
\usepackage{ifmtarg}
\usepackage{centernot}
\usepackage{empheq}
\usepackage{needspace}
\usepackage{colonequals}
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{arrows,positioning,shapes,shadows,trees}
\pagestyle{empty}
\begin{document}
FIGURE
\end{document}"""
counter = 0
for fig in re.findall(r'(\\begin\{figure.+?\\end\{figure\})', s, re.DOTALL):
    for r in re.findall(r'(\\caption\{.+?\})', fig):
        fig = fig.replace(r,'')
    o1 = open('test.tex','wr+')
    o1.write(figure.replace('FIGURE',fig).replace('\n\n','\n').replace('\n\n','\n').encode('utf-8'))
    o1.close()
    os.system('pdflatex test.tex')
    os.system('pdfcrop ./test.pdf')
    os.system('convert -density 1200 -resize 600x ./test-crop.pdf %s.png'% counter)
    os.remove('test.tex')
    os.remove('test.pdf')
    os.remove('test-crop.pdf')
    counter+=1
    
for r in re.findall(r'\\begin\{lstlisting\}(.+?)\\end\{lstlisting\}',s,re.DOTALL):
    s = s.replace(r'\begin{lstlisting}%s\end{lstlisting}'%r, '<source lang="python">%s</source>'%r)
for r in re.findall(r'\\begin\{notice\}\{(.+?)\}(.+?)\\end\{notice\}', s, re.DOTALL):
    s = s.replace(r'\begin{notice}{%s}%s\end{notice}'%(r[0], r[1]), '<h6>%s</h6><source lang="tex">%s</source>'%(r[0], r[1]))
for r in re.findall(r'\\begin\{note\}(.+?)\\end\{note\}',s,re.DOTALL):
    s = s.replace(r'\begin{note}%s\end{note}'%r, '<source lang="tex">%s</source>'%r)
for r in re.findall(r'\\section\{(.+?)\}', s):
    s = s.replace('\section{%s}'%r,'<h4>%s</h4>'%r)
for r in re.findall(r'\\subsection\{(.+?)\}', s):
    s = s.replace('\subsection{%s}'%r,'<h4>%s</h4>'%r)
for r in re.findall(r'\\subsubsection\{(.+?)\}', s):
    s = s.replace('\subsubsection{%s}'%r,'<h5>%s</h5>'%r)
for r in re.findall(r'\\textit\{(.+?)\}', s):
    s = s.replace(r'\textit{%s}'%r,'<em>%s</em>'%r)
for r in re.findall(r'\$(.+?)\$', s):
    s = s.replace(r'$%s$'%r,'<em>%s</em>'%r)
for r in re.findall(r'(\\begin\{itemize.*?\})(.+?)(\\end\{itemize.*?\})',s, re.DOTALL):
    s = s.replace(r'%s%s%s'%r, '<ul>%s</ul>'%r[1])
for r in re.findall(r'\item(.+?)\n',s,re.DOTALL):
    s = s.replace(r'\item%s'%r, '<li>%s</li>\n'%r)
for r in re.findall(r'<<(.+?)>>',s):
    s = s.replace('<<%s>>'%r, u'«%s»'%r)
for r in re.findall(r'\\texttt\{(.+?)\}', s):
    s = s.replace(r'\texttt{%s}'%r,'<em>%s</em>'%r)
for r in re.findall(r'\{\\bf(.+?)\}', s):
    s = s.replace(r'{\bf%s}'%r,r)
for r in re.findall(r'\\url\{(.+?)\}', s):
    s = s.replace(r'\url{%s}'%r , '<a href="%s" >%s</a>'%(r,r))
footcounter = 0 
foots = []
for foot in re.findall(r'\\footnote\{(.+?)\}', s):
    footcounter+=1
    foots.append(foot)
    s = s.replace(r'\footnote{%s}'%foot,'<sup>%s</sup>'%footcounter)
    
s+='<hr><ol>'
for f in foots:
    s+='<li>%s</li>\n'%f
s+='</ol>'

for text in re.findall(r'<source(.+?)</source>',s, re.DOTALL):
    tmp = text
    for r in re.findall(r'(<.+?>)', text):
        text = text.replace(r,'')
    s = s.replace(tmp,text)




s = s.replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n')
s = s.replace('\_','_')
s = s.replace('\Theta',u'Θ')
s = s.replace('\ldots',u'…')
s = s.replace('"---',u'—')
o.write(s.encode('utf-8'))
o.close()
