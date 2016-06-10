from planout.experiment import SimpleExperiment
from planout.ops.random import *

class estimationtask(SimpleExperiment):
  def assign(self, params, userid):
    params.nbars = UniformChoice(choices=[1,2,5,10], unit=userid)
    params.weight = UniformChoice(choices=[0], unit=userid)
    params.time = UniformChoice(choices=[1,2,3,4,5], unit=userid)
    params.a = UniformChoice(choices=[-.75,0,.75], unit=userid)
    return params;

