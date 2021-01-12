import speech_recognition as sr
from gtts import gTTS
import pyglet
import os, time
import datetime
import requests
import json

from run_server import JobForm



host = "http://127.0.0.1:5000/"

path_of_files = "assets/"


def convert_to_dict(obj):
  obj_dict = {
  }
  obj_dict.update(obj.__dict__)
  
  return obj_dict    



def parseSelectedJobNumber(text):
    
    if text == 'Cancel' or text == 'cancel':
        return 0
    elif text == '1' or text == 'One' or text == 'one':
        return 1
    elif text == '2' or text == 'Two' or text == 'two' or text == 'Tu':
        return 2
    elif text == '3' or text == 'Three' or text == 'three':
        return 3
    elif text == '4' or text == 'Four' or text == 'four':
        return 4
    elif text == '5' or text == 'Five' or text == 'five':
        return 5
    elif text == '6' or text == 'Six' or text == 'six':
        return 6
    elif text == '7' or text == 'Seven' or text == 'seven':
        return 7
    elif text == '8' or text == 'Eight' or text == 'eight':
        return 8
    elif text == '9' or text == 'Nine' or text == 'nine':
        return 9
    elif text == '10' or text == 'Ten' or text == 'ten':
        return 10
    elif text == '11' or text == 'Eleven' or text == 'eleven':
        return 11
    elif text == '12' or text == 'Twelve' or text == 'twelve':
        return 12
    else:
        return None




def speakOut(message):
    tts = gTTS(text=message, lang='en')
    ttsname=(path_of_files+"message.mp3")
    tts.save(ttsname)
    music = pyglet.media.load(ttsname, streaming = False)
    music.play()
    time.sleep(music.duration)
    os.remove(ttsname)
    
    
def listenForText():
    #voice recognition part
    text = None
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio=r.listen(source)
        print ("ok done!")
        
    try:
        text=r.recognize_google(audio)
        print ("You said : ["+text+"]")
        speakOut("You said : "+text)
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        speakOut("Google Speech Recognition could not understand audio")
         
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
        speakOut("Could not request results from Google Speech Recognition service")

    return text


def processJobForm(jonForm):
    
    NOT_REQUIRE = "NOT_REQUIRE"
    REQUIRED = "REQUIRED"
    
    if jonForm.first_name == REQUIRED:
        speakOut("Speak your first name")
        print("Speak your first name.")
        jonForm.first_name = listenForText()
        if jonForm.first_name == None:
            return None
            
    if jonForm.last_name == REQUIRED:
        speakOut("Speak your last name")
        print("Speak your last name.")
        jonForm.last_name = listenForText()
        if jonForm.last_name == None:
            return None
    
    if jonForm.father_name == REQUIRED:
        speakOut("Speak your father's name")
        print("Speak your father's name.")
        jonForm.father_name = listenForText()
        if jonForm.father_name == None:
            return None
    
    if jonForm.mother_name == REQUIRED:
        speakOut("Speak your mother name")
        print("Speak your mother name.")
        jonForm.mother_name = listenForText()
        if jonForm.mother_name == None:
            return None
    
    if jonForm.date_of_birth == REQUIRED:
        speakOut("Speak your date of birth")
        print("Speak your date of birth")
        jonForm.date_of_birth = listenForText();
        if jonForm.date_of_birth == None:
            return None
    
    if jonForm.permanent_address == REQUIRED:
        speakOut("Speak your permanent address")
        print("Speak your permanent address")
        jonForm.permanent_address = listenForText();
        if jonForm.permanent_address == None:
            return None
    
    if jonForm.corospondence_address == REQUIRED:
        speakOut("Speak your corospondence address")
        print("Speak your corospondence address.")
        jonForm.corospondence_address = listenForText();
        if jonForm.corospondence_address == None:
            return None
    
    if jonForm.high_school_passing_year == REQUIRED:
        speakOut("Speak your high school year")
        print("Speak your high school year")
        jonForm.high_school_passing_year = listenForText();
        if jonForm.high_school_passing_year == None:
            return None
    
    if jonForm.high_school_persentage == REQUIRED:
        speakOut("Speak your high school persentage")
        print("Speak your high school persentage")
        jonForm.high_school_persentage = listenForText();
        if jonForm.high_school_persentage == None:
            return None
    
    if jonForm.intermideate_passing_year == REQUIRED:
        speakOut("Speak your intermideate year")
        print("Speak your intermideate year")
        jonForm.intermideate_passing_year = listenForText();
        if jonForm.intermideate_passing_year == None:
            return None
    
    if jonForm.intermediate_persentage == REQUIRED:
        speakOut("Speak your intermediate persentage")
        print("Speak your intermediate persentage")
        jonForm.intermediate_persentage = listenForText();
        if jonForm.intermediate_persentage == None:
            return None
    
    if jonForm.bachelor_passing_year == REQUIRED:
        speakOut("Speak your bachelor year")
        print("Speak your bachelor year")
        jonForm.bachelor_passing_year = listenForText();
        if jonForm.bachelor_passing_year == None:
            return None
    
    if jonForm.bechelor_persentage == REQUIRED:
        speakOut("Speak your bechelor persentage")
        print("Speak your bechelor persentage")
        jonForm.bechelor_persentage = listenForText();
        if jonForm.bechelor_persentage == None:
            return None
    
    if jonForm.pg_passign_year == REQUIRED:
        speakOut("Speak your P.G. year")
        print("Speak your P.G. year")
        jonForm.pg_passign_year = listenForText();
        if jonForm.pg_passign_year == None:
            return None
    
    if jonForm.pg_persentage == REQUIRED:
        speakOut("Speak your pg persentage")
        print("Speak your pg persentage")
        jonForm.pg_persentage = listenForText();
        if jonForm.pg_persentage == None:
            return None
    
    if jonForm.marital_status == REQUIRED:
        speakOut("Speak your marital status")
        print("Speak your marital status")
        jonForm.marital_status = listenForText();
        if jonForm.marital_status == None:
            return None
    
    return jonForm




def uploadToServer(job_form):

    #index, job_title, job_description, first_name, last_name, father_name, mother_name, date_of_birth,
    #                            permanent_address, corospondence_address, high_school_passing_year, high_school_persentage, 
    #                            intermideate_passing_year, intermediate_persentage, bachelor_passing_year, bechelor_persentage,
    #                            pg_passign_year, pg_persentage, marital_status

    request_url = host+"submitt_job_form"
    request_data = {    'job_title':job_form.job_title,
                        'job_description':job_form.job_description,
                        'first_name':job_form.first_name,
                        'last_name':job_form.last_name,
                        'father_name':job_form.father_name,
                        'mother_name':job_form.mother_name,
                        'date_of_birth':job_form.date_of_birth,
                        'permanent_address':job_form.permanent_address,
                        'corospondence_address':job_form.corospondence_address,
                        'high_school_passing_year':job_form.high_school_passing_year,
                        'high_school_persentage':job_form.high_school_persentage,
                        'intermideate_passing_year':job_form.intermideate_passing_year,
                        'intermediate_persentage':job_form.intermediate_persentage,
                        'bachelor_passing_year':job_form.bachelor_passing_year,
                        'bechelor_persentage':job_form.bechelor_persentage,
                        'pg_passign_year':job_form.pg_passign_year,
                        'pg_persentage':job_form.pg_persentage,
                        'marital_status':job_form.marital_status
                        }
    print("Request :",request_data)
    print(type(request_data))
    request_result = requests.post(request_url,request_data)
    return request_result
    
    






request_url = host+"downlaod_all_forms_list"
request_result = requests.get(request_url)
print("Request Result :",request_result.text)
forms = json.loads(request_result.text)


jobForms = [JobForm] * len(forms)
    
index = 0;
for mjobForm in forms:
    #print(mjobForm)
    jobForm = JobForm(mjobForm[0], mjobForm[1], mjobForm[2], mjobForm[3], mjobForm[4], mjobForm[5],
                            mjobForm[6], mjobForm[7], mjobForm[8], mjobForm[9], mjobForm[10], mjobForm[11],
                                mjobForm[12], mjobForm[13], mjobForm[14], mjobForm[15], mjobForm[16], mjobForm[17], mjobForm[18])
    jobForms[index] = jobForm;
    index += 1
    
    print(jobForm.job_title)


 




login = os.getlogin
print ("You are logging from : "+login())



#speak project name
speakOut("Project: Voice based Form for blind")
print("Project: Voice based Form for blind")
#speak Total availble jobs
speakOut("Total availble jobs are " + str(len(jobForms)))
print("Total availble jobs are " + str(len(jobForms)))




jobIndex  = 0
for job in jobForms:
    
    jobIndex+=1
    
    #speak job index
    speakOut("Job number :" + str(jobIndex)) 
    print("Job number :" + str(jobIndex)) 
    
    #speak job Title
    speakOut("Job title:" + (job.job_title))
    print("Job title:" + (job.job_title))
    
    #speak job Description
    speakOut("Job description:" + (job.job_description))
    print("Job description:" + (job.job_description))
   




speakOut("Speak job number to apply")
print("Speak job number to apply")

text = listenForText()

jobNumber = parseSelectedJobNumber(text)

print("Job Number",end=" : ")
print(jobNumber)

if jobNumber == 0:
    speakOut("cancel by user.")
    print("cancel by user.")
    
elif jobNumber == None:
    speakOut("selected option in out of option range.")
    print("selected option in out of option range.")

else:
    if len(jobForms) >= jobNumber:
        selectedJobForm = jobForms[jobNumber-1]
        
        result  = processJobForm(selectedJobForm)
        
        if not result == None:
            speakOut("Form is completed please speak Yes to upload.")
            print("Form is completed please speak Yes to upload..")
            textChoice = listenForText()
            
            if textChoice == "Yes" or textChoice == "yes":
                request_result = uploadToServer(result)
                speakOut(request_result.text)
                print(request_result.text)
            else:
                speakOut("Form upload cancel")
                print("Form upload cancel")
            
        else:
            speakOut("Form data error.")
            print("Form data error.")
            
        
        
    else:
        speakOut("Selected job number is invalid. please try again")
        print("Selected job number is invalid. please try again")
        




