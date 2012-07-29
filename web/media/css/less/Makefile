# `make`: compiles less files into css/style.css
# `make watch`: watches for changes
# Requirements: watchr, lessc

STYLE_LESS = ./style.less
STYLE_CSS = ../style.css
LESS_COMPRESSOR ?= `which lessc`
WATCHR ?= `which watchr`

styles:
	lessc ${STYLE_LESS} > ${STYLE_CSS}

watch:
	echo "Watching LESS files..."
	ruby autocompiler.rb
