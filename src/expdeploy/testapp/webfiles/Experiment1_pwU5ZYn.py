from planout.experiment import SimpleExperiment
from planout.ops.random import *

class VotingTask(SimpleExperiment):
  def assign(self, params, userid):
    params.butto = UniformChoice(choices=['Signup', 'Join now', 'Just Do It', 'Make Account', 'Create Account', 'Welcome'],
      unit=userid)
    params.bu = UniformChoice(choices= ['#0059FF', '#FFA500','#1abc9c','#9b59b6','#e74c3c','#c0392b','#16a085','#2ecc71'],
      unit=userid)
    
    return params;

