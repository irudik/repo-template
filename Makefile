SUBDIRS = code latex

.PHONY: all clean check-template $(SUBDIRS)

all: $(SUBDIRS)

# latex depends on code so `make -j` builds them in order
latex: code

$(SUBDIRS):
	$(MAKE) -C $@

check-template:
	python3 tools/check_template_consistency.py

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
