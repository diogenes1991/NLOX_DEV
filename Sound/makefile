
all: create compile open

create: 
	./Sound.py
	
compile:
	pdflatex "Auto-Generated-Piece.tex"

open:
	okular "Auto-Generated-Piece.pdf" &
	audacity "Auto-Generated-Piece.wav" &
