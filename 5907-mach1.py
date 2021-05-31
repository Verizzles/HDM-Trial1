#################### ham cheese production model ###################



import ccm      
log=ccm.log(html=True)   
from ccm.lib.actr import *
from ccm.lib.actr.hdm import *
from rulecomp import *



    

class Subway(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    bread=ccm.Model(isa='bread',location='on_counter')
    cheese=ccm.Model(isa='cheese',location='on_counter')
    ham=ccm.Model(isa='ham',location='on_counter')
    breadtop=ccm.Model(isa='bread',location='on_counter')

class MotorModule(ccm.Model):     # create a motor module do the actions 
    def do_bread(self, env_obj, slot_name, slot_value):           # note that technically the motor module is outside the agent
                          # but it is controlled from within the agent, i.e., it bridges the cognitive and the environment
        print ("work")
        x = self.parent.parent[env_obj]
        y = self.parent.parent.x[slot_name]
        setattr(x, y, slot_value)
        #self.parent.parent.bread.location='on_plate'    # self=MotorModule, parent=MyAgent, parent of parent=Subway
    def do_cheese(self):     
        yield 0.1                   # yield refers to how long the action takes, but cognition can continue while waiting for an action to complete
        print ("fuck")
        self.parent.parent.cheese.location='on_plate'   # in this case the motor actions make changes to the environment objects
    def do_ham(self):     
        yield 0.1
        print ("you")
        self.parent.parent.ham.location='on_plate'
    def do_breadtop(self):
        yield 0.1
        print ("work")
        self.parent.parent.breadtop.location='on_plate'




class MyAgent(ACTR):    
    focus=Buffer()
    
    retrieval=Buffer()   
    memory=HDM(retrieval, noise=0.0)
    motor=MotorModule()
    rule=RuleCompilation()

    memory.clear()
    
    def init():
        #eventually figure out how to generate this info from environment and Instructions
        memory.add('isa:bread location:on_counter cue:start goal:on_plate')
        memory.add('isa:cheese location:on_counter cue:bread goal:on_plate')
        memory.add('isa:ham location:on_counter cue:cheese goal:on_plate')
        memory.add('isa:breadtop location:on_counter cue:ham goal:on_plate')
        memory.add('isa:finished cue:breadtop location:on_counter')
        memory.add('state:action location:on_counter step:bread action:do_bread goal:on_plate')
        memory.add('state:action location:on_counter step:cheese action:do_cheese goal:on_plate')
        memory.add('state:action location:on_counter step:ham action:do_ham goal:on_plate')
        memory.add('state:action location:on_counter step:breadtop action:do_breadtop goal:on_plate')
        
        focus.set('begin')

    def start_sandwich(focus='begin'):
        print ('start_sandwich')  
        memory.request('cue:start location:on_counter isa:? goal:on_plate')    
        focus.set('remember')
   
    def remember_steps(focus='remember', retrieval='cue:?cue isa:?isa location:on_counter goal:on_plate'):
        print ('remember_steps',cue,isa)   
        memory.request('state:action location:on_counter step:?isa action:? goal:on_plate')
        focus.set('act') 

    
    def act_steps(focus='act', retrieval='state:action location:on_counter step:?step action:?action goal:?goal'):
        
        joe = rule.runaction(action, step, goal)
        eval(joe)
        memory.add('isa:?step location:on_plate action:?action')
        memory.request('cue:?step isa:? location:on_counter')      
        
        focus.set('remember')

    def finished (focus='remember', retrieval='isa:finished cue:?step location:on_counter'):
        print ('finished')   
        focus.set('stop')
        
        print ("I have made a ham and cheese sandwich") 


    def stop_production(focus='stop'):  # wait for the action to complete before stopping
        #print "I have made a ham and cheese sandwich"
        self.stop()


tim=MyAgent()
env=Subway()
env.agent=tim 
ccm.log_everything(env)

env.run()
ccm.finished()
