from DB.DB_Controller import ASAP_DB

class Car():
    def __init__(self, brand:str, car_name:str, type:str, car_number:str, pin_number:str, img_path:str = None):
        self.car_number = car_number
        self.brand = brand
        self.car_name = car_name
        self.type = type
        self.pin_number = pin_number

        self.battery = 0
        self.destroied = 0
        self.isrented = 0

        self.img_path = img_path
        self.pos = '0, 0'


class CarDB(ASAP_DB):
    def __init__(self):
        super().__init__()
        self.car_dict = {}
        self.car_brand = {}
        self.car_name = {}
        self.car_type = {}
        self.init_db()

    def add_car(self, car:Car):
        self.update_data(car)
        columns = "car_number, brand, car_name, type, pin_number, destroied, is_rented, img_path, battery, pos"
        value = f"'{car.car_number}', '{car.brand}', '{car.car_name}', '{car.type}', '{car.pin_number}', '{car.destroied}', '{car.isrented}', '{car.img_path}', '{car.battery}', '{car.pos}'"
        self.insert_values('car', columns, value)
    
    def update_data(self, car:Car):
        if car.car_number not in self.car_dict:
            self.car_dict[car.car_number] = car
        
            if car.brand not in self.car_brand:
                self.car_brand[car.brand] = [car.car_number]
            else:
                self.car_brand[car.brand].append(car.car_number)
            if car.car_name not in self.car_name:
                self.car_name[car.car_name] = [car.car_number]
            else:
                self.car_name[car.car_name].append(car.car_number)
            if car.type not in self.car_type:
                self.car_type[car.type] = [car.car_number]
            else:
                self.car_type[car.type].append(car.car_number)        
        
    def get_stat_info(self, info_type='all'):
        data = {}
        if info_type == 'all':
            cars = self.get_data('car', 'car_number, car_name')
        elif info_type == 'brand':
            cars = self.get_data('car', 'car_number, brand')
        elif info_type == 'type':
            cars = self.get_data('car', 'car_number, type')
        else:
            return Exception('Invalid info_type')
        
        for car in cars:
            key = car[1]
            value = car[0]
            if key not in data.keys():
                data[key] = [value]
            else:
                data[key].append(value)

        return data, self.car_name

    def remove_car(self, car:Car):
        if car.car_number in self.car_dict:
            self.car_brand[car.brand].remove(car.car_number)
            self.car_name[car.car_name].remove(car.car_number)
            del(self.car_dict[car.car_number])
            if len(self.car_name[car.car_name])==0:
                del(self.car_name[car.car_name])
            if len(self.car_brand[car.brand])==0:
                del(self.car_brand[car.brand])

        self.delete_values('car', f'car_number="{car.car_number}"')

        
    def init_db(self):
        self.car_dict = {}
        self.car_brand = {}
        self.car_name = {}
        self.car_type = {}
        data = self.get_data('car')

        for car in data:
            car_number, brand, car_name, type, pin_number, destroied, isrented, img_path, battery, pos = car
            vehicle = Car(brand, car_name, type, car_number, pin_number, img_path)
            vehicle.destroied = destroied
            vehicle.isrented = isrented
            vehicle.battery = battery
            if pos==None:
                vehicle.pos = '0, 0'
            else:
                vehicle.pos = pos
            self.update_data(vehicle)

