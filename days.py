import re


import datetime
from openpyxl.utils import datetime as to_ex



PRE_COMPIE = re.compile(r'\d+')



def __cell_to_date(date_cell_value):
    """セルのデータをdatetimeの日付（day)にする"""
    if isinstance(date_cell_value ,datetime.datetime):return date_cell_value.day
    elif isinstance(date_cell_value,int):return to_ex.from_excel(date_cell_value).day
    print(f'{date_cell_value}は日付に変換できませんでした')
    
    
def __cell_to_time(time_cell_value):
    """時間帯を数値に変換して大枠の時間帯を判定する"""
    def chenge_time_to_timetype(time_int:int)->int:
        if 7 <= time_int < 12 :return 1
        if 12 <= time_int < 24 :return 2
        return 0
    
    if isinstance(time_cell_value,float):return chenge_time_to_timetype(int(time_cell_value *10))
    if isinstance(time_cell_value,str):
        if result := PRE_COMPIE.match(time_cell_value): return chenge_time_to_timetype(int(result.group(0)))
        else:return 0
        
        
        

class HopspitalInfo:
    
    
    def __init__(self,hospital_name:str,hospital_num:str,corse_type:str,stmac_serch_type:str) -> None:
        self.hos_name = hospital_name
        self.hos_num = hospital_num
        self.corse = corse_type
        self.stmac = stmac_serch_type
        
        
    def __eq__(self, other: object) -> bool:
        return self.hos_num == other.hos_num and self.corse == other.corse and self.stmac == other.stmac 
    
    
    def __repr__(self) -> str:
        return f'{self.hos_name},{self.corse}:::{self.stmac}'
    
    
    
    

class AtDay():
    
    
    def __init__(self,date_value,time_value,hos_info: HopspitalInfo) -> None:
        self.date_value = __cell_to_date(date_value)
        self.time_type = __cell_to_time(time_value)
        self.raw_date_time = [date_value,time_value]
        self.hos_info = hos_info
        
        
    def __eq__(self, __value: object) -> bool:
        """継承先のクラス（希望日と予約枠）が同一日で同じ時間帯かどうか判定する"""
        if self.hos_info != __value.hos_info : return False
        
        first = self.date_value == __value.date_value
        second = self.time_type == __value.time_type or 0 == self.time_type | 0  == __value.time_type
        
        if first == True and second ==True :
            return True
        else:  
            return False
        

    def __repr__(self):
        return f'{self.date_value}:::{self.time_type}:::{self.hos_info}'
        


        

class HopeDay(AtDay):
    """社員の希望日"""
    
    def __init__(self,date_value,time_value,my_hos_info:HopspitalInfo) -> None:
        AtDay.__init__(self,date_value=date_value,time_value=time_value,hos_info=my_hos_info)
        self.who = None
        
        
        

    
   
    
class Reservation(AtDay):
    """病院からの予約枠"""
    
    def __init__(self,date_value,time_value,hos_info:HopspitalInfo):
        super().__init__(date_value,time_value,hos_info)
        self.registry_menber = {} #key = Emp value=emp.hope_days
        self.commitment_emp = None
        
        
    def emp_into_registry_menbers(self,this_emp):
        for at_day in this_emp.my_hope_days:
            if at_day == self:
                self.registry_menber[this_emp] = at_day
                this_emp.set_reservation_day.append(self)
                
    
    
    def lottery_setup(self):
        """registry_menberから一人選ぶ"""
        if len(self.registry_menber) == 0  or self.commitment_emp == None :return None
        
        #最も枠に入りずらい社員を選ぶ
        result_emp =  min(
            [(this_emp.evaluatin(),this_emp) for this_emp in self.registry_menber.keys()],
            key= lambda x:x[0]
        )[1]
        
        self.commitment_emp = result_emp
        print(
            result_emp,
            self
        )
        
        # 決まった社員にお手付きの枠へ自身を削除するよう依頼
        result_emp.call_notify(self)
        self.registry_menber.clear()
        
        return result_emp
    
    
    def unregist_emp(self,this_emp):
        """empを外す"""
        if this_emp in self.registry_menber:
            del self.registry_menber[this_emp]
            
    
    def __len__(self):
        return len(self.registry_menber)
    
    
    def __repr__(self) -> str:
        return super().__repr__()
    



class CentralControl:
    """枠と社員のやり取りを制御するクラス"""
    
    def __init__(self):
        self.all_emps = {}
        self.all_reservation = []
        self.completed= {}
    
    def add_emp(self,this_emp):
        if this_emp in self.all_emps:self.all_emps[this_emp] = this_emp.my_hope_days
    
    def add_reservation(self,reservation_day:Reservation):
        if reservation_day in self.all_reservation: self.all_reservation.append(reservation_day)
    
    def __mix_setup(self):
        """社員と予約枠を紐づける"""    
        for emp in self.all_emps.keys():
            for reservation in self.all_reservation:
                reservation.emp_into_registry_menbers(emp)
        print('登録完了')
    
    def main(self):
        
        def check(this_list:list[reversed])-> bool:
            for reserved in this_list:
                if len(reserved) != 0 : return True
            else:return False
            
            
        self.__mix_setup()
        
        temp_list = [day for day in self.all_reservation]
        
        i = 1
        
        while check(temp_list):
            
            for reserved in temp_list:
                if len(reserved) == i:
                    self.completed[reserved.lottery_setup()] = reserved
                    i = 1
                    break
            else:
                i +=1
                
        print('終了')
        print(self.completed)
                
            
        
        
        
        
        
            