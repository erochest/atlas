
PY =D:/Python22/python.exe
SAXON =$(PY) D:/bin/saxon.py
FOP =$(PY) D:/bin/fop.py
HHC ="D:/HTML Help Workshop/hhc.exe"
VALIDATE =$(PY) D:/bin/validate.py

HTML = /dtds/docbook/xsl/html/chunk.xsl
HTMLHELP = /dtds/docbook/xsl/htmlhelp/htmlhelp.xsl
FO = /dtds/docbook/xsl/fo/docbook.xsl

HTMLOPTS =
HTMLHELPOPTS =
FOOPTS =

SOURCE = devel.xml

# generic targets

# for xsl
# html
%.html : %.xml
	$(SAXON) $< $(HTML) $(HTMLOPTS)

# htmlhelp
%.hhp : %.xml
	$(SAXON) $< $(HTMLHELP) $(HTMLHELPOPTS)

%.chm : %.hhp
	$(HHC) $<

# pdf
%.fo : %.xml
	$(SAXON) -o $@ $< $(FO) $(FOOPTS)

%.pdf: %.fo
	$(FOP) -fo $< -pdf $@

# top-level targets

all: validate html htmlhelp 

html: index.html

htmlhelp: devel.chm

pdf: devel.pdf

index.html: $(SOURCE)
	$(SAXON) $< $(HTML) $(HTMLOPTS)

# abstract maintenance targets
validate:
	$(VALIDATE) $(SOURCE)

clean:
	rm -f *~

distclean:
	rm -fr *.html

