from dataclasses import dataclass


@dataclass
class SpeedCarService:
    profile_width:float
    profile_height:float
    diameter:float
    frequency_turns_per_min: list

    def _post_init_(self):
        nominal_radius = 0.0254*(self.diameter/2)+(self.profile_width/1000)*(self.profile_height/100)
        static_radius = nominal_radius*self.tire_crumpling_ratio()
        dynamic_radius = nominal_radius-((nominal_radius-static_radius)/3)

    def __tire_crumpling_ratio(self):
        '''
            Возвращает коефициент смятия шин относительно высоты профиля колеса
        '''
        if(self.profile_height>=90):
            return 0.8
        elif(self.profile_height<=50):
            return 0.85
        else:
            return 0.814285714
    def __calculate_speed_array(self, ):