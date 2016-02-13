from planout.experiment import SimpleExperiment
from planout.ops.random import *

class VotingTask(SimpleExperiment):
  def assign(self, params, userid):
    params.button_text = UniformChoice(choices=["I'm voting", "I'm a voter"],
      unit=userid)
    return params;

