from request_interphase import API_INTERPHASE
import dearpygui.dearpygui as dpg

web_link = "https://doctors.sanitasremota.com/account/login"
api_link = "https://api-doctors.sanitasremota.com"


test_user = "D20DF935-AB7D-4392-8F9B-3FA266868FA0"

# GUI window base efinitions #
global width, height, windowName
g_Width = 1024
g_Height = 768
g_WindowName = "HTTPS Development GUI"

global user_connection_data
user_connection_data:API_INTERPHASE = None


global patient_uuid
patient_uuid = ""

def show_user_data(parent):
    global user_connection_data
    dpg.add_text(parent=parent,tag="user_information",default_value="User Information",pos=[40,40],show=True)
    dpg.add_text(parent=parent,tag="user_firstName",default_value="First Name: ",pos=[40,80],show=True)
    dpg.add_text(parent=parent,tag="user_lastName",default_value="Last Name: ",pos=[40,120])
    dpg.add_text(parent=parent,tag="user_email",default_value="Email: ",pos=[40,160])
    dpg.add_text(parent=parent,tag="user_phone",default_value="Phone: ",pos=[40,200])
    dpg.add_text(parent=parent,tag="user_birthDate",default_value="Birth Date: ",pos=[40,240])
    dpg.add_text(parent=parent,tag="user_weight",default_value="Weight: ",pos=[40,280])
    dpg.add_text(parent=parent,tag="user_height",default_value="Height: ",pos=[40,320])
    dpg.add_text(parent=parent,tag="user_id",default_value="Id: ",pos=[40,360])
    dpg.add_text(parent=parent,tag="user_role",default_value="Role: ",pos=[40,400])
    #dpg.add_text(parent=parent,tag="user_token",default_value="token: ",pos=[40,440],wrap=800)


def update_user_data():
    global user_connection_data

    user_data:dict = user_connection_data.get_user_data()

    for items in user_data.keys():
        if(dpg.does_item_exist("user_" + items)):
            dpg.set_value("user_" + items, dpg.get_value("user_" + items) + " " + str(user_data[items]))


def filter_patients(sender,user_data,data):
    update_patients("patient_list",user_data)

def show_patients(parent:str):
    dpg.add_text(parent=parent,tag="patient_list_text",default_value="Patients in platform: " + web_link,pos=[40,40],show=True)
    dpg.add_text(parent=parent,tag="patient_list_text_search",default_value="Search User: ",pos=[40,80],show=True)
    dpg.add_input_text(parent=parent, width=240,hint="Search box",pos=[160,80],show=True,callback=filter_patients)
    dpg.add_listbox(parent=parent,tag="patient_list",pos=[40,120],width=920,num_items=32,callback=update_patient_data)

def update_patients(listbox_tag:str,filter:str):
    global user_connection_data

    list_data:list = []
    for users_data in user_connection_data.get_user_list_cache():
        if(filter in users_data["name"]):
            list_data.append(users_data["name"] + " " + users_data["last_name"] + " - " + users_data["uuid"])

    dpg.configure_item(listbox_tag,items=list_data)


def update_patient_data():
    global user_connection_data
    global patient_uuid

    if(dpg.does_item_exist("selected_patient")):
        dpg.delete_item("selected_patient")
        
    if(dpg.does_item_exist("selected_patient_measures")):
        dpg.delete_item("selected_patient_measures")

    create_patient_tabs()

    _, uuid = str(dpg.get_value("patient_list")).split(" - ")
    patient_uuid = uuid
    user_data:dict = user_connection_data.get_patient_data(uuid)


    for items in user_data.keys():
        if(dpg.does_item_exist("patient_" + items)):
            dpg.set_value("patient_" + items, dpg.get_value("patient_" + items) + " " + str(user_data[items]))

    
    measurements_patient:list = user_connection_data.get_last_user_measurement(uuid,user_connection_data.get_user_uuid())

    for items in measurements_patient:
        if(dpg.does_item_exist("patient_measurement_" + items["name"])):

            if("value" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " " + str(items["value"]))

            if("height" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " " + str(items["height"]))

            if("weight" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " " + str(items["weight"]))

            if("diastolicPressure" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " Diastolic: " + str(items["diastolicPressure"])
                              + " Systolic: " + str(items["systolicPressure"]))

            if("patientTemp" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " " + str(items["patientTemp"]))

            if("spo2" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " " + str(items["spo2"]))

            if("hemoglobin" in items.keys()):
                dpg.set_value("patient_measurement_" + items["name"], dpg.get_value("patient_measurement_" + items["name"]) + " " + str(items["hemoglobin"]))

def show_patient_data(parent:str):
    dpg.add_text(parent=parent,tag="patient_information",default_value="Patient Information",pos=[40,40],show=True)
    dpg.add_text(parent=parent,tag="patient_name",default_value="First Name: ",pos=[40,80],show=True)
    dpg.add_text(parent=parent,tag="patient_last_name",default_value="Last Name: ",pos=[40,120])
    dpg.add_text(parent=parent,tag="patient_email",default_value="Email: ",pos=[40,160])
    dpg.add_text(parent=parent,tag="patient_phone",default_value="Phone: ",pos=[40,200])
    dpg.add_text(parent=parent,tag="patient_birth_date",default_value="Birth Date: ",pos=[40,240])
    dpg.add_text(parent=parent,tag="patient_Weight",default_value="Weight: ",pos=[40,280])
    dpg.add_text(parent=parent,tag="patient_uuid",default_value="Id: ",pos=[40,320])
    dpg.add_text(parent=parent,tag="patient_gender_description",default_value="Gender: ",pos=[40,360])
    dpg.add_text(parent=parent,tag="patient_BloodType",default_value="Blood Type: ",pos=[40,400])
    

patient_measurements:str = ["Blood Pressure","Oxygen saturation", "Weight", "Height", "Glucose", "Cholesterol", "Triglycerides", "Uric acid", "Lactate", "Ketone", "Hemoglobin"]

def show_patient_measurements(parent:str):
    dpg.add_text(parent=parent,tag="patient_measurement_Blood Pressure",default_value="Blood Pressure Measurement: ",pos=[40,40],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Oxygen saturation",default_value="Oxygen saturation Measurement: ",pos=[580,40],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Weight",default_value="Weight Measurement: ",pos=[40,80],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Height",default_value="Height Measurement: ",pos=[580,80],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Glucose",default_value="Glucose Measurement: ",pos=[40,120],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Cholesterol",default_value="Cholesterol Measurement: ",pos=[580,120],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Triglycerides",default_value="Triglycerides Measurement: ",pos=[40,160],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Uric acid",default_value="Uric acid Measurement: ",pos=[580,160],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Lactate",default_value="Lactate Measurement: ",pos=[40,200],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Ketone",default_value="Ketone Measurement: ",pos=[580,200],show=True)
    dpg.add_text(parent=parent,tag="patient_measurement_Hemoglobin",default_value="Hemoglobin Measurement: ",pos=[40,240],show=True)


    dpg.add_text(parent=parent,tag="patient_add_measurement_text",default_value="Add Measurements: ",pos=[40,280],show=True)
    dpg.add_combo(parent=parent,tag="patient_add_measurement",items=patient_measurements, user_data=parent,callback=add_patient_measurements,pos=[160,280])


def add_patient_measurements(sender:str,data,user_data):
    
    if(dpg.does_item_exist("patient_measurements_box")):
        dpg.delete_item("patient_measurements_box")

    dpg.add_child_window(tag="patient_measurements_box",parent=user_data,width=950,height=400,pos=[24,320])
         
    if (data == patient_measurements[0]):
        dpg.add_text(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure_systolic_text",default_value="Systolic Pressure Value: ",pos=[40,40],show=True)
        dpg.add_text(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure_diastolic_text",default_value="Systolic Pressure Value: ",pos=[40,80],show=True)
        dpg.add_text(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure_bpm_text",default_value="Beats per Minute Value: ",pos=[40,120],show=True)

        dpg.add_input_int(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure_systolic",pos=[300,40],show=True,width=240)
        dpg.add_input_int(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure_diastolic",pos=[300,80],show=True,width=240)
        dpg.add_input_int(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure_bpm",pos=[300,120],show=True,width=240)

        dpg.add_button(parent="patient_measurements_box",tag="patient_add_measurement_Blood_Pressure",label="Upload Measurements",pos=[40,160],show=True,width=240,callback=upload_Blood_Pressure)


def upload_Blood_Pressure(sender,data,user_data):
    global user_connection_data
    global patient_uuid

    systolic:int = dpg.get_value("patient_add_measurement_Blood_Pressure_systolic")
    diastolic:int  = dpg.get_value("patient_add_measurement_Blood_Pressure_diastolic")
    mean:float  = format(( (2 * systolic + diastolic) / 3),'.2f')
    bpm:int  = dpg.get_value("patient_add_measurement_Blood_Pressure_bpm")

    if(user_connection_data.add_blood_pressure(patient_uuid,user_connection_data.get_user_uuid(),systolic,diastolic,mean,bpm)):
        update_patient_data()



def create_patient_tabs():
    with dpg.tab(label="Patient data", tag="selected_patient", parent="main_tab_bar"):
        show_patient_data("selected_patient")

    with dpg.tab(label="Patient Measures", tag="selected_patient_measures", parent="main_tab_bar"):
        show_patient_measurements("selected_patient_measures")





# Tab Bar definition and implementation #
def mainTabBarSetup(parent:str):
    with dpg.tab_bar(tag="main_tab_bar",parent=parent):
        with dpg.tab(label="User Data", tag="user_data", parent="main_tab_bar"):
            show_user_data("user_data")

        with dpg.tab(label="List of patients", tag="user_patients", parent="main_tab_bar"):
            show_patients("user_patients")


def show_password(sender:str,data,user_data):
    _,text_name = sender.split("_")

    dpg.configure_item(text_name,password=(not dpg.get_item_configuration(text_name)["password"]))


def delete_window(sender):
    dpg.delete_item(dpg.get_item_parent(sender))

def connect_user(sender,data,user_data):
    global user_connection_data

    user = dpg.get_value(user_data[0]) 

    password = dpg.get_value(user_data[1]) 

    if((user != "") and ("@" in user) and (password != "")):
        user_connection_data = API_INTERPHASE(api_link,user,password)
    else:
        dpg.set_value("log_in_text","The user or the password have incorrect type.")
        return

    if(user_connection_data):
        update_user_data()
        update_patients("patient_list","")
        delete_window(sender)
    else:
        dpg.set_value("log_in_text","The user or the password does not exist.")

    
# Context for GUI generation #
dpg.create_context()

with dpg.window(label="log_in_window", tag="log_in_window",width=0.25*g_Width, height=0.3*g_Height,pos=[0.35*g_Width,0.2*g_Height],menubar=False,no_title_bar=True,no_resize=True):
    dpg.add_input_text(parent="log_in_window",tag="email",hint="Enter Email",width=220,height= 60,pos=[20,40])
    dpg.add_input_text(parent="log_in_window",tag="password",hint="Input Password",height= 60,password=True,pos=[20,90])
    dpg.add_button(parent="log_in_window",tag="show_password",label="show",pos=[200,90],width=40,callback=show_password)
    dpg.add_button(parent="log_in_window",tag="log_in_button",label="Login",width=80,pos=[30,140],callback=connect_user,user_data=["email","password"])
    dpg.add_button(parent="log_in_window",tag="log_in_close_button",label="Close",width=80,pos=[140,140],callback=delete_window)
    dpg.add_text(parent="log_in_window",tag="log_in_text",label="",pos=[20,180],wrap=200)

with dpg.window(label="main_window", tag="main_window", width=g_Width, height=g_Height,menubar=False,no_title_bar=True,no_move=True,no_resize=True,no_bring_to_front_on_focus=True):
    mainTabBarSetup("main_window")

dpg.create_viewport(title=g_WindowName, width=1024, height=768,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()