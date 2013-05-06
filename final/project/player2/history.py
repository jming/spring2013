import game_interface
from collections import defaultdict


class History():
   def __init__(self, view):
	self.plant_bonus = (20, False) #Will update once we ate the first nutritious plant. Boolean indicates whether it has been updated
	self.plant_penalty = (10, False) #Will update once we ate the first poisonous plant
	self.life_per_turn = (1, False) #Will update after the first move
	self.observation_cost = (1, False) #Will update after we tested for the first time
	self.positions = []
	self.energies = []	

	self.exist_plant = [] # indicates whether there is a plant
        self.tested = []
        self.test_results = []
	self.eats = []  #Boolean values
	self.eat_results = [] #if the bool=True in eat_or_not, store the eat result, True=Nutritious
        self.updateStatus(view)

   def appendPlantInfo(self, exist, get_image, test_result, eat):
        self.exist_plant.append(exist)
        self.tested.append(get_image)
        self.test_results.append(test_result)
        self.eats.append(eat)

   def updateStatus(self, view):
      self.positions.append((view.GetXPos(),view.GetYPos()))
      self.energies.append(view.GetLife())

      if len(self.energies) > 1:
	     prev_energy = self.energies[-2]
	     energy = self.energies[-1]
	     eat_result = False
	     if len(self.eats) > 0 and self.eats[-1]:
	       if prev_energy < energy: eat_result = True
	     self.eat_results.append(eat_result)

             if (not self.tested[-1]) and (not self.eats[-1]): #Just moved, not test, no eat
	          self.life_per_turn = (prev_energy - energy, True)
             elif self.tested[-1] and (not self.eats[-1]): #Tested but didn't eat
	          (life, updated) = self.life_per_turn
	          if updated: 
	            self.observation_cost = (prev_energy - energy - life, True)
             elif self.eats[-1] and self.tested[-1]: #Tested and ate
	          (life, updated) = self.life_per_turn
	          (cost, updated2) = self.observation_cost
	          if updated and updated2: 
	             if eat_result: self.plant_bonus = (energy-prev_energy+life+cost,True)
	             else: self.plant_penalty = (prev_energy-energy-life-cost, True)
      

      """
      if len(self.energies) > 1:
        # print 'energies, ', self.energies
        if self.exist_plant[-1] and self.eat_results[-1]: print 'Ate nutritious'
        if not self.exist_plant[-1]: print 'No plant'
        elif (not self.eat_results[-1]): print 'Ate poisonous'
      """

      #print 'Position:', self.positions[-1]
      #print '\n\n Hooray start'
      #print 'exist plant', self.exist_plant
      #print 'tested', self.tested
      #print 'eats', self.eats
      #print 'eat result', self.eat_results[-1]
      #print 'plant bonus', self.plant_bonus
      #print 'plant penalty', self.plant_penalty
      #print 'observation cost ',self.observation_cost
      #print 'life per turn', self.life_per_turn
      #print 'Hooray end\n\n'
   
   def getEatResults(self):
      return self.eat_results

   def updateDecisions(self, eat):
      self.eats.append(eat)

   def getPositions(self):
      return self.positions
  
   def getBonus(self):
      bonus, _ = self.plant_bonus
      return bonus

   def getLifePerTurn(self):
      lpt, _ = self.life_per_turn
      return lpt
   
