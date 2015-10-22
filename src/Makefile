# Tudor Berariu, 2015

.phony: clean stats

stats: stats.tex
	pdflatex stats.tex
	rm stats.aux stats.log
	gnome-open stats.pdf

stats.tex: game_server.py
	python game_server.py

clean:
	find . -name "stats.*" -print0 | xargs -0 rm -f
	find . -name "*~" -print0 | xargs -0 rm -f
	find . -name "*.pyc" -print0 | xargs -0 rm -f
