from django.shortcuts import render
from SIHRE.forms import inputForm
from SIHRE.models import dbms1
from django.core import mail
from Backend.Interface.main import Forecast
import datetime


def index(request):
    return render(request, 'home.html')


def check(request):
    temp1=inputForm()
    return render( request,'inputvalues.html',{'form':temp1})

def result(request):
    if request.method == "POST":
        user_input_values = request.POST.copy()
    patientData = user_input_values.dict()

    # Deleting the metdata in the dictionary as it is not required
    del patientData['csrfmiddlewaretoken']

    Name = patientData.pop('Patient_name')
    Id = patientData.pop('Patient_id')

    # Converting the values that are as a string to lists
    convertStringToList(patientData)

    # Predicting for the user data
    obj = Forecast(patientData)

    output = obj.get()

    temp = dbms1(pt_id=Id, pt_name=Name,pt_output=output,created_at=datetime.datetime.now())
    temp.save()
    db = dbms1.objects.all()
    if 1 in output:
        connection = mail.get_connection()
        connection.open()
        email = mail.EmailMessage(
            'Sepsis Detected !',
            'Patient : ' + Name + '\nPatient Id : ' + Id + '\nSepsis Result : Positive',
            'nandan980633@gmail.com',
            ['imanpalsingh@gmail.com'],
        )
        connection.send_messages([email])
        connection.close()

    # output="output" #remove this
    context = {'db': db,'output': output,'pt_name':Name,'pt_id': Id,'created_at': datetime.datetime.now()}
    return render(request, 'result_ml.html', context)




def information(request):
    return render(request,'information.html',)


#author of this function is Imanpal Singh
def convertStringToList(dictionary):
    '''
    Function to convert a dictionary of strings to dictionary of lists

    Input
    =====

    `dictionary` : `dict`

    dictionary to convert

    Output
    ======
    `None`

    Example
    =======

    >>> convertStringToList(patientData)

    THe dictionary like `{ 'HR' : '1,2,3,4' , 'SBP' : '1,2,3,4' }`

    will be converted to required format as

    `{ 'HR' : [1,2,3,4] , 'SBP' : [1,2,3,4] }`

    '''
    for key in dictionary.keys():
        values = [float(val) for val in dictionary[key].split(',')]
        dictionary[key] = values




