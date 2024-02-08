from requests import post
from datetime import datetime

# Class that handles login to the api and basic connection data#
class LOGIN_INTERPHASE:
    """
    Parameters
    ----------
    email: str
    password: str
    api_header: str

    Returns
    ----------
    LOGIN_INTERPHASE : object

    Notes
    ----------
    Gets login basic connection credentials from the given server.
    """

    __api_login_header:str = ""
    __conection = False

    # Store credentials in case reconection is needed #
    __login:dict = {
        "email" : "",
        "password" : ""
    }

    # Store login data gotten from server describing the user #
    __login_data:dict = {
        "uuid": "",
        "firstname":"",
        "lastname":"",
        "email":"", 
        "phone":"",
        "birthdate":"",
        "weight":"",
        "height":"",
        "id": "",
        "role": "",
        "token": ""
    }

    def __init__(self,email:str,password:str,api_header:str):

        # Format payload for request #
        self.__login["email"] = email
        self.__login["password"] = password
        self.__api_login_header = api_header

        # Try to log in using the api header if everything is ok set connection to true #
        try:
            request = post(self.__api_login_header,json = self.__login)

            if(request.ok):
                self.__login_data = request.json()
                self.__conection = True
            else:
                print("Check error: " + str(request.status_code))

        except:
            self.__conection = False
            print("Fatal Error")


    def _get_connection_status(self)->bool:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        bool : connection status

        Notes
        ----------
        Private method for using in parent class.
        """
        return self.__conection

    def get_user_data(self)->dict:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        dict : connection 

        Notes
        ----------
        Private method for using in parent class.
        """

        return self.__login_data
    
    def get_user_uuid(self)->str:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        str : user uuid 

        Notes
        ----------
        Private method for using in parent class.
        """

        return self.__login_data["uuid"]

    def _get_authentification(self)->str:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        str : token

        Notes
        ----------
        Returns the bearer token from the logged user.
        """
        return self.__login_data["token"]
    



# Class that handles Doctor functions in the api and basi getters for it #
class DOCTOR_INTERPHASE():
    """
    Parameters
    ----------
    api_base_header:str

    Returns
    ----------
    DOCTOR_INTERPHASE : object

    Notes
    ----------
    Gets doctor data from API endpoints.
    """

    __api_base_header:str = ""
    
    __conection_token = ""

    __routes_dictionary:dict = {
        "statistics":"/getUserStatisticsDoctor",
        "notifications":"/getUserNotifications",
        "emergency":"/getUserEmergencyNotifications",
        "personal":"/getUserInfo"
    }

    __payload_data:dict = {
        "statistics":{
            "uuid": ""
        },
        "notifications":{
            "uuid":"",
            "measurement_type":"",
            "notification_level":"",
            "notification_status":""
        },
        "emergency":{
            "uuid":"",
            "notification_level":"",
            "notification_status":""
        },
        "personal":{
            "uuid": ""
        }
    }

    __user_data:dict = {
        "statistics": {},

        "notifications": [],

        "emergency": [],

        "personal": {}
    }

    def __init__(self,api_base_header:str,token:str):

        self.__api_base_header = api_base_header

        self.__conection_token= {"Authorization": ("Bearer "+ str(token))}


    def _update_doctor_info(self,uuid:str)->None:
        """
        Parameters
        ----------
        api_base_header:str

        Returns
        ----------
        None.

        Notes
        ----------
        Gets doctor data from API endpoints.
        """

        # Post request and get info from the different endpoints #
        for routes in self.__routes_dictionary:
            self.__payload_data[routes]["uuid"] = uuid

            try:
                response = post(self.__api_base_header + self.__routes_dictionary[routes],headers=self.__conection_token,json=self.__payload_data[routes])

                if(response.ok):
                    self.__user_data[routes] = response.json()
                else:
                    raise Exception(("Exception getting data from route: "+ str(routes) +", make better logger"))

            except:
                print("Fatal error")

    def get_statistics(self)->dict:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        dict: info of statistics

        Notes
        ----------
        Gets doctor data from API endpoints.
        """
        return self.__user_data["statistics"]
            
    def get_notifications(self)->dict:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        dict: info of notifications

        Notes
        ----------
        Gets doctor data from API endpoints.
        """
        return self.__user_data["notifications"]
    
    def get_emergency(self)->dict:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        dict: info of emergecy

        Notes
        ----------
        Gets doctor data from API endpoints.
        """
        return self.__user_data["emergency"]
    
    def get_personal(self)->dict:
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        dict: info of doctor

        Notes
        ----------
        Gets doctor data from API endpoints.
        """
        return self.__user_data["personal"]
    

# Class that handles Patient functions in the api and basic getters for it #
class PATIENT_INTERPHASE():

    """
    Parameters
    ----------
    api_base_header:str

    Returns
    ----------
    PATIENT_INTERPHASE : object

    Notes
    ----------
    Gets patient data from API endpoints.
    """

    __api_base_header = ""

    __conection_token = ""

    # Routes needed for accessing all the users on the database #
    __all_users_routes_dictionary:dict = {
        "campaign":"/getCampaigns",
        "users":"/getUsers"
    }

    __user_list:list = []

    __all_users_payload_data:dict = {
        "campaign":{
            "uuid":"",
            "campaignStatus":""
        },
        "users":{
            "type_user_id":0,
            "uuid_edit":""
        }
    }


    # Routes needed for accesing all user measurements #
    __user_routes_dictionary:dict = {
        "user_info":"/getUserInfo",
        "user_last_measurments":"/getLastMeasurements",
        "user_measurement":"/getMeasurement",
        "add_measurement":"/addMeasurement"
    }

    __user_payload_data:dict = {
        "user_info":{
            "uuid": ""
        },

        "user_measurement":{
            "uuid_user":"",
            "month":"",
            "year":"",
            "type_measurement":""
        },

        "user_last_measurments":{
            "uuid_user":"",
            "month":"",
            "year":"",
            "uuid_edit":""
        },

        "add_measurement" :{
            "uuid_user":"",
            "value":"",
            "uuid_device":"0F3B2F2A-4621-4CA5-8314-1542DA15AABC",
            "measurement_date":"",
            "type_measurement":"",
            "uuid_edit":""
        }       
    }

    __user_last_measurments:list = []

    __user_measurment:dict = {
        "Blood Pressure":[],
        "Oxygen saturation":[],
        "Weight":[],
        "Height":[],
        "Glucose":[],
        "Cholesterol":[],
        "Triglycerides":[],
        "Uric acid":[],
        "Lactate":[],
        "Ketone":[],
        "Hemoglobin":[]
    }

    def __init__(self,api_base_header:str,token:str):

        self.__api_base_header = api_base_header
        self.__conection_token = {"Authorization": ("Bearer "+ str(token))}

    def get_user_list(self,user_type:int,uuid_edit:str="")->list:
        """
        Parameters
        ----------
        user_type:int
        uuid_edit:str

        Returns
        ----------
        Fromatted user List.

        Notes
        ----------
        Gets type of user list.

        """

        self.__all_users_payload_data["users"]["type_user_id"] = user_type
        self.__all_users_payload_data["users"]["uuid_edit"] = uuid_edit

        try:
            response = post(self.__api_base_header + self.__all_users_routes_dictionary["users"],headers=self.__conection_token,json=self.__all_users_payload_data["users"])

            if(response.ok):
                 self.__user_list = response.json()
            else:
                print("User list could not be fetched")

            return self.__user_list
        
        except:
            raise("Fatal ERROR")

             
    def get_user_list_cache(self):
        """
        Parameters
        ----------
        None.

        Returns
        ----------
        List of users with characteristics

        Notes
        ----------
        Gets user list from buffer

        """

        return self.__user_list

    def get_patient_data(self,uuid:str)->dict:
        """
        Parameters
        ----------
        uuid:str

        Returns
        ----------
        User data dict

        Notes
        ----------
        Gets info of the required user

        """

        self.__user_payload_data["user_info"]["uuid"] = uuid


        try:
            response = post(self.__api_base_header + self.__user_routes_dictionary["user_info"],headers=self.__conection_token,json=self.__user_payload_data["user_info"])

            if(response.ok):
                 user_data = response.json()[0]
            else:
                print("User data could not be fetched")

            return user_data
        
        except:
            print("Fatal ERROR")

    def get_user_measurment(self,user_id:str,type_measurement:str)->list:
        """
        Parameters
        ----------
        user_id:str
        type_measurement:str

        Returns
        ----------
        List of measurements.

        Notes
        ----------
        Get user measurement list of one type.

        """

        self.__user_payload_data["user_measurement"]["uuid_user"] = user_id
        self.__user_payload_data["user_measurement"]["type_measurement"] = type_measurement

        try:
            response = post(self.__api_base_header + self.__user_routes_dictionary["user_measurement"],headers=self.__conection_token,json=self.__user_payload_data["user_measurement"])
            
            if(response.ok):
                self.__user_measurment[type_measurement] = response.json()
            else:
                print("Measurement cant be retrieven")

            return self.__user_measurment[type_measurement]
        
        except:
            raise("Fatal ERROR")



    def get_last_user_measurement(self,user_id:str,uuid_edit:str)->list:
        """
        Parameters
        ----------
        user_id:str
        uuid_edit:str

        Returns
        ----------
        List of measurements.

        Notes
        ----------
        Get user measurement list of one type.

        """

        self.__user_payload_data["user_last_measurments"]["uuid_user"] = user_id
        self.__user_payload_data["user_last_measurments"]["uuid_edit"] = uuid_edit

        try:
            response = post(self.__api_base_header + self.__user_routes_dictionary["user_last_measurments"],headers=self.__conection_token,json=self.__user_payload_data["user_last_measurments"])
            
            if(response.ok):
                self.__user_last_measurments = response.json()
            else:
                print("Measurements cant be retrieven")

            return self.__user_last_measurments
        
        except:
            raise("Fatal ERROR")



    def add_measurement(self,user_id:str,uuid_edit:str,type_measurement:str,measurement_data:str,uuid_device:str="0F3B2F2A-4621-4CA5-8314-1542DA15AABC")->bool:
        """
        Parameters
        ----------
        user_id:str
        type_measurement:str
        measurement_data:str
        uuid_edit:str

        Returns
        ----------
        bool: measurementupload

        Notes
        ----------
        Get user measurement list of one type.

        """

        self.__user_payload_data["add_measurement"]["uuid_user"] = user_id
        self.__user_payload_data["add_measurement"]["value"] = measurement_data
        self.__user_payload_data["add_measurement"]["measurement_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__user_payload_data["add_measurement"]["uuid_device"] = uuid_device
        self.__user_payload_data["add_measurement"]["type_measurement"] = type_measurement
        self.__user_payload_data["add_measurement"]["uuid_edit"] = uuid_edit


        try:
            response = post(self.__api_base_header + self.__user_routes_dictionary["add_measurement"],headers=self.__conection_token,json=self.__user_payload_data["add_measurement"])
            
            if((response.ok) and (response.json()[0]["success"] == 1)):
                return True
            else:
                print("Cannot add measurement")

            return False
        
        except:
            raise("Fatal ERROR")


    def add_blood_pressure(self,user_id:str,uuid_edit:str,systolic:int,diastolic:int,mean_pressure:float,bpm:int,uuid_device:str="0F3B2F2A-4621-4CA5-8314-1542DA15AABC")->bool:
        
        formatted_value = str(systolic)+ "," + str(diastolic) + ","  + str(mean_pressure) + "," + str(bpm) + ",,,,,"

        return self.add_measurement(user_id,uuid_edit,"Blood Pressure",formatted_value,uuid_device)




    def add_spo2(self,user_id:str,spo2:int,BPM:int,PI:float,uuid_device:str="0F3B2F2A-4621-4CA5-8314-1542DA15AABC"):
        
        formatted_value = str(spo2)+ "," + str(BPM) + ","  + str(PI)

        self.add_measurement(user_id,"Oxygen saturation",formatted_value,uuid_device)


    def add_weight(self,user_id:str,weight:int,bmi:int,unit:str="kg",uuid_device:str="0F3B2F2A-4621-4CA5-8314-1542DA15AABC"):

        if("Height" in self.__user_last_measurments[6]):
            bmi = weight/(self.__user_last_measurments[6] * self.__user_last_measurments[6])

        formatted_value = str(weight)+ "," + unit + ","  + str(bmi)

        self.add_measurement(user_id,"Weight",formatted_value,uuid_device)

    def add_height(self,user_id:str,height:int,unit:str="kg",uuid_device:str="0F3B2F2A-4621-4CA5-8314-1542DA15AABC"):
        
        formatted_value = str(height)+ "," + unit

        self.add_measurement(user_id,"Height",formatted_value,uuid_device)

    def add_glucose(self,user_id:str,value:int,unit:str="mg/dL",type:str="Generic",code="",uuid_device:str=""):
        
        formatted_value = str(value)+ "," + unit + ","  + type + "," + "Glucose" + ",-" + str(code)

        self.add_measurement(user_id,"Glucose",formatted_value,uuid_device)

    def add_cholesterol(self,user_id:str,value:int,unit:str="mg/dL",type:str="Generic",code="",uuid_device:str=""):
        
        formatted_value = str(value)+ "," + unit + ","  + type + "," + "Cholesterol" + ",-" + str(code)

        self.add_measurement(user_id,"Cholesterol",formatted_value,uuid_device)


    def add_triglycerides(self,user_id:str,value:int,unit:str="mg/dL",type:str="Generic",code="",uuid_device:str=""):
        
        formatted_value = str(value)+ "," + unit + ","  + type + "," + "Triglycerides" + ",-" + str(code)

        self.add_measurement(user_id,"Triglycerides",formatted_value,uuid_device)


    def add_uric_acid(self,user_id:str,value:int,unit:str="mg/dL",type:str="Generic",code="",uuid_device:str=""):
        
        formatted_value = str(value)+ "," + unit + ","  + type + "," + "Uricacid" + ",-" + str(code)

        self.add_measurement(user_id,"Uric acid",formatted_value,uuid_device)


    def add_lactate(self,user_id:str,value:int,unit:str="mg/dL",type:str="Generic",code="",uuid_device:str=""):
        
        formatted_value = str(value)+ "," + unit + ","  + type + "," + "Lactate" + ",-" + str(code)

        self.add_measurement(user_id,"Lactate",formatted_value,uuid_device)


    def add_Ketone(self,user_id:str,value:int,unit:str="mmol/L",type:str="Generic",code="",uuid_device:str=""):
        
        formatted_value = str(value)+ "," + unit + ","  + type + "," + "Ketone" + ",-" + str(code)

        self.add_measurement(user_id,"Ketone",formatted_value,uuid_device)


    def add_Hemoglobin(self,user_id:str,value:int,unit:str="g/dL",uuid_device:str="0F3B2F2A-4621-4CA5-8314-1542DA15AABC"):
        
        formatted_value = str(value)+ "," + unit

        self.add_measurement(user_id,"Hemoglobin",formatted_value,uuid_device)



# Class that handles Patient functions in the api and basic getters for it #
class API_INTERPHASE(LOGIN_INTERPHASE,DOCTOR_INTERPHASE,PATIENT_INTERPHASE):

    """
    Parameters
    ----------
    api_base_header:str
    user:str
    password:str

    Returns
    ----------
    API_INTERPHASE : object

    Notes
    ----------
    Used for interphasing with different endpoints
    """

    def __init__(self,api_base_header:str,user:str,password:str):
        LOGIN_INTERPHASE.__init__(self,user,password,api_base_header + "/login")

        if(self._get_connection_status()):
            DOCTOR_INTERPHASE.__init__(self,api_base_header,self._get_authentification())

            self._update_doctor_info(self.get_user_uuid())

            PATIENT_INTERPHASE.__init__(self,api_base_header,self._get_authentification())

            self.get_user_list(4,self.get_user_uuid())
