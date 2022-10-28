from datetime import datetime
from typing import List


class Person:
    def __init__(self, first_name, last_name, middle_name=None, birth_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birth_date = birth_date
    
    @property
    def full_name(self):
        fullname = self.last_name + ' ' + self.first_name
        if self.middle_name is not None:
            fullname += ' ' + self.middle_name        
        return fullname
    
    @full_name.setter
    def full_name(self, new):
        '''Вводить по порядку ФИО через пробел'''
        fullname = new.split(' ')
        if len(fullname) == 3:
            self.middle_name = fullname[2]
        self.last_name, self.first_name = fullname[:2]
    

class Employee(Person):
    def __init__(self, first_name, last_name, middle_name=None, position=None):
        super().__init__(first_name, last_name, middle_name)
        self.position = position
        self.Calendar = EmployeeCalendar()


class EmployeeCalendar:
    # рабочее время сотрудника по умолчанию
    __start_work = datetime.strptime('09:00', '%H:%M')
    __end_work = datetime.strptime('18:00', '%H:%M')
    
    def __init__(self):
        # мноежество встреч сотрудника
        self.meetings = set()

    def get_work_hours(self):
        '''Возвращает рабочее время сотрудника(может быть разным среди сотрудников)'''
        return self.__start_work, self.__end_work
    
    def set_work_hours(self, new_start, new_end):
        self.__start_work = datetime.strptime(new_start, '%H:%M')
        self.__end_work = datetime.strptime(new_end, '%H:%M')

    def get_free_hours(self, meetings=None, start=None, end=None):
        '''Возвращает свободные временные слоты (в пределах рабочего времени сотрудника)'''
        free_hours = set()
        if start is None and end is None:
            start, end = self.get_work_hours()
        if meetings is None:
            meetings = sorted(self.meetings)

        for m_start, m_end in meetings:
            if start < m_start:
                free_hours.add((start, m_start))
                start = m_end
            else:
                # в случае вложенных отрезков необходимо брать максимум из двух значений
                # это понадобится для поиска свободных слотов для списка сотрудников
                start = max(m_end, start)
        
        if start < end:
            free_hours.add((start, end))
        return sorted(free_hours)

    def set_meeting(self, start, end):
        '''Назначает встречу'''       
        meet_start = datetime.strptime(start, '%H:%M')
        meet_end = datetime.strptime(end, '%H:%M')
        
        # проверить что встреча проводится в рабочее время
        if meet_end <= meet_start:
            raise ValueError("Incorrect time interval")
        elif meet_start < self.__start_work or meet_end > self.__end_work:
            raise ValueError("The meeting is outside of working hours")                

        free_hours = self.get_free_hours()
        
        for slot_start, slot_end in free_hours:
            if slot_start <= meet_start and slot_end >= meet_end:
                self.meetings.add((meet_start, meet_end))
                print('Meeting is set up!')
                break
        else:
            print("No free slot was found for this meeting")
            
    def get_common_slots(self, employees: List[Employee]):
        total_start = max([e.Calendar.get_work_hours()[0] for e in employees])
        total_end = min([e.Calendar.get_work_hours()[1] for e in employees])
        
        total_meetings = set()
        for e in employees:
            total_meetings |= e.Calendar.meetings

        total_meetings = sorted(total_meetings)        
        total_free_hours = self.get_free_hours(meetings=total_meetings, start=total_start, end=total_end)

        return total_free_hours    