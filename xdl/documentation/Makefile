# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXBUILDOPTS		?= "-a"
SPHINXBUILD		?= sphinx-build
SPHINX_APIDOC	?= sphinx-apidoc
SOURCEDIR		= ./src
BUILDDIR		 = ./build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) --help

.PHONY: help Makefile

clean:
	rm -rf $(BUILDDIR)
	python generate_standard_docs.py

cleanall:
	 @read -p "!!! That would remove all files under .\src !!! Are you sure? " -r; \
        if [[ $$REPLY =~ ^[Yy] ]]; then \
            rm -rf $(BUILDDIR); \
			rm -rf $(SOURCEDIR); \
        fi

apidoc:
	@$(SPHINX_APIDOC) --separate --doc-project "API Reference" --output $(SOURCEDIR) ..\xdl

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:clean
	@$(SPHINXBUILD) -M $@ . "$(BUILDDIR)" $(SPHINXBUILDOPTS) $(O)
