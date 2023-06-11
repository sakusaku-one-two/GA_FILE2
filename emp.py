from days import HopeDay

class Emp:
    
    def __init__(self,name,emp_num,my_hope:list[HopeDay]):
        self.name = name
        self.emp_num = emp_num
        self.my_hope_days = my_hope
        self.my_hash = hash(name+emp_num)
        self.set_reservation_day = []
        self.result_reservation = None
        
        
        
    def evaluatin(self)-> float:
        """Reservation  クラスのlottery_setup   methodから呼び出せる関数"""
        return sum(
            [1/len(this_reserved) for this_reserved in self.set_reservation_day]
        ) / len(self.set_reservation_day)
    
    def call_notify(self,result_reservation):
        for this_day in self.set_reservation_day:
            this_day.unregist_emp(self)
        self.set_reservation_day.clear()
        self.result_reservation = result_reservation
        
    
    def __hash__(self) -> int:
        return self.my_hash
    
    def __eq__(self, other: object) -> bool:
        return self.my_hash == other.my_hash
        
        