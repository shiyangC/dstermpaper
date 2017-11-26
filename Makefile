# makefile for pdf2latex
name=main

#open: allfontpdf
open: pdf
		open -a Preview ${name}.pdf;
pdf:
		pdflatex ${name}; 
		pdflatex ${name}.tex; 
		bibtex ${name}
		pdflatex ${name}.tex; 
allfontpdf:
	#bibtex ${name}
	latex ${name}.tex
	dvips ${name}
	bibtex ${name}
	ps2pdf -dSubsetFonts=true -dEmbedAllFonts=true -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress -sPAPERSIZE=letter ${name}.ps ${name}.pdf
clean: 
	rm -rf ${name}.aux ${name}.bbl ${name}.log ${name}.blg\
	 ${name}.out ${name}.out.bak ${name}.ps ${name}.dvi *~
