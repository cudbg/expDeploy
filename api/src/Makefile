LIBRARY_FILES = \
    interface.js

../example/api.js: $(LIBRARY_FILES)
	node_modules/.bin/smash $(LIBRARY_FILES) > ../example/api.js

api.js: $(LIBRARY_FILES)
	node_modules/.bin/smash $(LIBRARY_FILES) | node_modules/.bin/uglifyjs - -c -m -o $@