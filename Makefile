bin = .venv/bin
.PHONY: prototype

prototype: prototype-build
	$(bin)/python -m http.server 8081 -d prototype/_site

prototype-build:
	rm -rf prototype/_site
	$(bin)/python prototype/build.py
