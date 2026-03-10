SUBDIRS = code latex

.PHONY: all clean thorny thorny-dry-run thorny-resume thorny-report $(SUBDIRS)

all: $(SUBDIRS)

# latex depends on code so `make -j` builds them in order
latex: code

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done

thorny:
ifeq ($(strip $(TASK)),)
	$(error Usage: make thorny TASK="..." [SCOPE="path1 path2"] [VERIFY="make -C code/foo"] [MAX_PLANNER_CALLS=2] [MAX_CODER_TURNS=6] [PLANNER_EFFORT=medium] [QUALITY_GATE=90])
endif
	python3 tools/thorny_loop/main.py --task "$(TASK)" $(if $(SCOPE),--scope $(SCOPE),) $(if $(VERIFY),--verify "$(VERIFY)",) $(if $(MAX_PLANNER_CALLS),--max-planner-calls $(MAX_PLANNER_CALLS),) $(if $(MAX_CODER_TURNS),--max-coder-turns $(MAX_CODER_TURNS),) $(if $(PLANNER_EFFORT),--planner-effort $(PLANNER_EFFORT),) $(if $(QUALITY_GATE),--quality-gate $(QUALITY_GATE),)

thorny-dry-run:
ifeq ($(strip $(TASK)),)
	$(error Usage: make thorny-dry-run TASK="..." [SCOPE="path1 path2"] [VERIFY="make -C code/foo"] [MAX_PLANNER_CALLS=2] [MAX_CODER_TURNS=6] [PLANNER_EFFORT=medium] [QUALITY_GATE=90])
endif
	python3 tools/thorny_loop/main.py --task "$(TASK)" --dry-run $(if $(SCOPE),--scope $(SCOPE),) $(if $(VERIFY),--verify "$(VERIFY)",) $(if $(MAX_PLANNER_CALLS),--max-planner-calls $(MAX_PLANNER_CALLS),) $(if $(MAX_CODER_TURNS),--max-coder-turns $(MAX_CODER_TURNS),) $(if $(PLANNER_EFFORT),--planner-effort $(PLANNER_EFFORT),) $(if $(QUALITY_GATE),--quality-gate $(QUALITY_GATE),)

thorny-resume:
ifeq ($(strip $(RUN)),)
	$(error Usage: make thorny-resume RUN="timestamp_slug")
endif
	python3 tools/thorny_loop/main.py --resume "$(RUN)"

thorny-report:
ifeq ($(strip $(RUN)),)
	$(error Usage: make thorny-report RUN="timestamp_slug")
endif
	python3 tools/thorny_loop/main.py --report "$(RUN)"
