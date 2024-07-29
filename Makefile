bin = .venv/bin
.PHONY: prototype

prototype:
	rm -rf prototype/_site
	$(bin)/python prototype/build.py
	$(bin)/python -m http.server 8081 -d prototype/_site
