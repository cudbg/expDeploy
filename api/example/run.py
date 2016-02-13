


import importlib;


VotingExperiment = getattr(importlib.import_module("VotingTask"), "VotingTask")

exp = VotingExperiment(userid=14);
print(exp.get("button_text"));