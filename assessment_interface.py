from abc import ABC, abstractmethod


class assessment_interface(ABC):

     @ abstractmethod
     def __init__(self):
         pass

     @ abstractmethod
     def assess(self):
         pass
