from os import system
import subprocess


print(subprocess.check_output("make ../example/api.js", shell=True))
print(subprocess.check_output("cp ../example/api.js ../../src/expdeploy/gpaas/templates", shell=True))
print(subprocess.check_output("cp ../example/api.js ../../../pfunk_vldb16/user_experiments/measure_bars/api.js", shell=True))