.PHONY: test docs

PYTHON := python
DOCS_DIR := doc
RST_SRCDIR := $(DOCS_DIR)/source
RST_BUILDDIR := $(DOCS_DIR)/build
PYTHON_SRCDIR := chatbot_utils

all: docs

autodoc:
	sphinx-apidoc -E -M -o $(RST_SRCDIR) $(PYTHON_SRCDIR) -f

docs: autodoc
	make clean html -C $(DOCS_DIR)

clean:
	[ -d $(RST_BUILDDIR) ] && rm -rf $(RST_BUILDDIR)
