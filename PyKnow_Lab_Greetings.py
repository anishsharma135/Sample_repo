#!/usr/bin/env python
# coding: utf-8

# [Docs](https://docplayer.net/94508494-Pyknow-documentation-release-roberto-abdelkader-martinez-perez.html)

# In[1]:


get_ipython().system('pip install https://github.com/buguroo/pyknow/archive/v1.7.0.tar.gz')


# # Facts: The Data
# - Fact: A subclass of dictionary
# - Fact can have arbitrary number of fields

# In[2]:


from pyknow import Fact
f = Fact('8', a=1, b=1)
print(f['a'])
print(f[0])
print(f)


# ## Declaring facts
# ### DefFacts()
# reset() method invokes DefFact() and adds yielded facts to working memory
# ### declare(Fact(a='x'))
# - adds a fact to working memory
# - The Fact has a Field a with value x

# # Rules: The Knowledge
# ## salience
# This value, by default0, determines the priority of the rule in relation to the others. Rules with a higher salience willbe fired before rules with a lower on

# In[3]:


from pyknow import Rule
@Rule(Fact(a='a')) # RHS: antecedent, the if condition
def _():
  # LHS: consequent, then do something, 
  pass


# # Agenda
# list of rules to be executed

# # Field Constraints

# ## W() wildcard Field Constraint

# In[4]:


# match if a fact is declared with a field mykey
from pyknow import Rule
from pyknow import W
@Rule(Fact(mykey=W()))
def _():
  pass


# ## L() a literal Field Constraint

# In[5]:


from pyknow import L
@Rule(Fact(name=L('Alice')))
def _():
  pass


# ## P() Predicate Field Constraint

# In[6]:


# Match if some fact is declared whose first parameter is an instance of int
from pyknow import Rule
from pyknow import P
@Rule(Fact(P(lambda x: isinstance(x, int))))
def _():
  pass


# ## Composing Field Constraints (FCs)

# ### AND FC &
# Match if some fact is declared whose first parameter is an instance of int

# In[7]:


from pyknow import Rule
from pyknow import P
# Match if key x of Point is a value between 0 and 255.
@Rule(Fact(x=P(lambda x: x >= 0) & P(lambda x: x <= 255)))
def _():
  pass


# ### OR FC |

# In[8]:


from pyknow import L
@Rule(Fact(name=L('Alice') | L('Bob')))
def _():
  pass


# ### NOT FC ~

# In[9]:


@Rule(Fact(name=~L('Charlie')))
def _():
  pass


# # Name Bindings

# ## << Operator
# Any pattern and some Field Constrainsts (FCs) can be binded to a name using the **<<** operator.
# Deprecated since version 1.2.0: Use MATCH object instead

# In[13]:


# The first value of the matching fact will be binded to the name
# myvalue and passed to the function when fired.
@Rule(Fact("myvalue" << W()))
def _(myvalue):
  pass
# Above is exactly same as following
@Rule(Fact(MATCH.myvalue))
def _(myvalue):
  pass


# ### MATCH
# The MATCH objects helps generating more readable name bindings. Is syntactic sugar for a Wildcard Field Constraint binded to a name.

# In[14]:


from pyknow import MATCH
@Rule(Fact(MATCH.name))
def _(name):
  pass


# In[15]:


# The whole matching fact will be binded t0 f1 and passed to
# the function when fired.
@Rule('myfact' << Fact())
def _(myfact):
  pass
# Above is exactly same as following
from pyknow import AS
@Rule(AS.myfact << Fact(W()))
def _(myfact):
  pass


# # Example Traffic Lights

# In[16]:


from random import choice
from pyknow import *


class Light(Fact):
    """Info about the traffic light."""
    pass

# KnowledgeEngine 
# You ES will subclass KnowledgeEngine
# 1. Decorate methods to define rules of the ES
# 2. Instantiate
# 3. Reset system (reset() method) : prep for execution
# 4. declare input facts (delare() method)
# 5. run the engine (run method)
class RobotCrossStreet(KnowledgeEngine):
    # The Rule is callable
    # Will match with every instace of 'Light' Fact
    # Rules have two components
    # 1. LHS: antecedent~ Conditions on which rule must be fired
    # 2. RHS: consequent~ Set of actions the must be carried out
    @Rule(Light(color='green')) # LHS
    def green_light(self):
        print("Walk") # RHS

    @Rule(Light(color='red')) #LHS
    def red_light(self):
        print("Don't walk") # RHS

    @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow'))) # LHS
    def cautious(self, light):
        print("Be cautious because light is", light["color"]) #RHS


# ## initialize the knowledge engine

# In[17]:


engine = RobotCrossStreet()


# ## reset()

# In[18]:


engine.reset()


# ## get_rules

# In[19]:


engine.get_rules()


# ## declare()

# In[ ]:


# Declare a fact
engine.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))


# ## run()

# In[ ]:


engine.run()


# # Example Greetings

# In[20]:


from pyknow import KnowledgeEngine
from pyknow import Rule
from pyknow import Fact
from pyknow import DefFacts
from pyknow import W # Wildcard Field Constraint
from pyknow import NOT # matching the absence of a given Fact/Pattern
from pyknow import MATCH


# In[32]:


class Greetings(KnowledgeEngine):

  # Default Facts need to be present for the system to work
  # All Facts inside DefFact are called every time system is reset
  @DefFacts()
  def _initial_action(self):
    # following will be executed by reset()
    print('DefFacts') 
    yield Fact(action='greet') 
  
  @Rule(Fact(action='greet'))
  def ask_name(self):
    print('ask_name')
    self.declare(Fact(name=input("What's your name?")))

  @Rule(Fact(action='greet'))
  def ask_location(self):
    print('ask_location')
    self.declare(Fact(location=input("where are you from?")))

  @Rule(Fact(action='greet'))
  def ask_weather(self):
    print('ask_weather')
    self.declare(Fact(temperature=input("how is the temperature today?")))
    
  @Rule(Fact(action='greet'))
  def ask_age(self):
    print('ask_age')
    self.declare(Fact(age=input("what is the age?")))
      
    

  @Rule(Fact(action='greet'), 
        Fact(name=MATCH.name),
        # Fact(name='name' << W()), # same as Fact(name=Match.name)
        # Fact(location="location" << W()))
        Fact(age=MATCH.age),
        Fact(location=MATCH.location),
        Fact(temperature=MATCH.temperature))
  def greet(self, name, temperature, location, age):
    print('greet')
    print("Hi %s! your age is %s %s is cold in %s?"%(name,age, temperature, location)) 
 


# In[33]:


greetings_engine = Greetings()
greetings_engine.reset()
print('run')
greetings_engine.run()


# ## get_deffacts()

# In[ ]:


greetings_engine.get_deffacts()


# ## get_rules

# In[ ]:


greetings_engine.get_rules()

