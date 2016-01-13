LIBRARY_FILES = \
    interface.js

api.js: $(LIBRARY_FILES)
	node_modules/.bin/smash $(LIBRARY_FILES) | node_modules/.bin/uglifyjs - -c -m -o $@