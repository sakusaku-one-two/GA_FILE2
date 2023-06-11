from abc import abstractclassmethod,ABCMeta

from emp import *
from days import *

from import_excell import *


class IState(Meta = ABCMeta):

    @abstractclassmethod
    def __init__(self,contlorer) -> None:
        pass
    @abstractclassmethod
    def do(self):
        pass
    
    
class MixToAction(IState):
    
    def __init__(self,controler):
        self.controler = controler
    
    def do(self):
        pass
   
class Creater(IState):
    
    def __init__(self,controler):
        self.controler = controler
        
    
        
        
    def __create_emp(self):
        def create_hope_day(this_row):
            pass
        pass
    
    def __create_reservation(self):
        pass
    
        
    def do(self):
        
        central_control = CentralControl()
        self.controler.central_controler = central_control
        
        
        self.controler.at_state = MixToAction(self.controler)
   
    
    
class Load(IState):
    
    def __init__(self,controler):
        self.controler = controler
        
    def __col_names(self,this_sheet):
        row = this_sheet.row[1]
        return {i.value:i.column for i in row}
        
    
    def do(self):
        
        wb = op.load_workbook(self.controler.excell_path)
        self.controler.wb = wb
        emp_sheet = wb.get_sheet_by_name('社員リスト')
        hos_sheet = wb.get_sheet_by_name('予約枠')
        self.controler.sheets= {'社員リスト':[emp_sheet,self.__col_names(emp_sheet)],
                                 '予約枠':[hos_sheet,self.__col_names(hos_sheet)]}

        self.controler.at_state = Creater(self.controler)
        
    
    
    
    
class Controler:
    
    def __init__(self,load_excell_path):
        self.excell_path = load_excell_path
        self.at_state:IState = Load(self)
        
    def do_action(self):
        
        while self.at_state != None:
            self.at_state.do()
            