import json

with open('linear-1.json') as f:
	s = f.read()
	print(s)
	print(json.loads(s))