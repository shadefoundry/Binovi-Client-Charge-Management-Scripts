#DK, Feb 13th, 2018

from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
 
file = '/Users/student2/Desktop/importCleanup.csv'
df = pd.read_csv(file, header=None, skiprows=0)
print("READ SUCCESS")


class NewUser:
    def __init__(self,pid, fname, lname, bday, bmonth, byear, email, gemail, sex, handedness, startweek, expweeks,
                username, password, guardfname, guardlname):
        self.pid = pid
        self.fname = fname
        self.lname = lname
        self.bday = bday
        self.bmonth = bmonth
        self.byear = byear
        self.email = email
        self.gemail = gemail
        self.sex = sex
        self.handedness = handedness
        self.startweek = startweek
        self.expweeks = expweeks
        self.username = username
        self.password = password
        self.guardfname = guardfname
        self.guardlname = guardlname
    


### GLOBALS
dumpList = []
validEmails=[]
patList = []
combinedList=[]
parentList = []
childList = []
invalidList = []
invalidReasonList = []

####POPULATE LIST
def fillPatientList():
    h=0
    for h in range(len(df.index)):
        dumpList.append(NewUser(df.iloc[h,0],df.iloc[h,2], df.iloc[h,3], df.iloc[h,4], df.iloc[h,5], df.iloc[h,6], df.iloc[h,7],
               df.iloc[h,8], df.iloc[h,9], df.iloc[h,10], df.iloc[h,11], df.iloc[h,12], df.iloc[h,13], df.iloc[h,14],
               df.iloc[h,15], df.iloc[h,16]))

fillPatientList()


def validateEmail():
    i = 0
    for i in range(len(dumpList)):
        x = 0
        matchCount = 0
        for x in range(len(dumpList)): 
            if dumpList[i].email == dumpList[x].email and dumpList[i].pid != dumpList[x].pid:
                matchCount +=1
                if matchCount > 1:
                    
                    invalidList.append(dumpList[i])
                    invalidReasonList.append("Duplicate Email Found")
        
        ### Validate Email by checking for @ and . in email string
        if '@' in str(dumpList[i].email):
            if '.' in str(dumpList[i].email):
                validEmails.append(dumpList[i])
                


def validateUsernames():
    o = 0
    for o in range(len(validEmails)):
        selected = validEmails[o]
        if ' ' in str(selected.username):
            invalidList.append(dumpList[o])
            invalidReasonList.append("Space Found In Username")
        elif " " in str(selected.username):
            invalidList.append(dumpList[o])
            invalidReasonList.append("Space Found In Username")
            
        elif len(selected.username) < 4:
            invalidList.append(dumpList[o])
            invalidReasonList.append("Username Too Short")
                
        p=0
        usermatchCount = 0
        for p in range(len(dumpList)):
            if str(selected.username) == str(dumpList[p].username) and selected.pid != dumpList[p].pid:
                usermatchCount +=1
                if usermatchCount > 1:
                    invalidList.append(dumpList[o])
                    invalidReasonList.append("Duplicate Username Found")
                
        patList.append(validEmails[o])
        




#Seperate validated users from users with missing data
def filterAllPatients():
   
    errors = 0
    h=0
    
    validateEmail()
    validateUsernames()
    
    for h in range(len(patList)):
        if h!=0 or str(patList[h]) != "NaN":
            if patList[h].fname != "" and patList[h].lname != "":
                if str(patList[h].sex) == "Female" or str(patList[h].sex).lower() == "Male":
                    try:
                        if int(patList[h].byear) < 2004:
                            if str(patList[h].email) != "nan":
                                parentList.append(patList[h])
                            
                            else:
                                invalidList.append(patList[h])
                                invalidReasonList.append("Invalid Email")
                        
                        elif int(patList[h].byear) >= 2004:
                            
                            if str(patList[h].gemail) != "nan":
                                childList.append(patList[h])
                            elif str(patList[h].email) != "nan":
                                childList.append(patList[h])
                            else:
                                invalidList.append(patList[h])
                                invalidReasonList.append("Invalid Guardian Email")
            
                    except ValueError:
                        #do nothing
                        errors +=1 
                else:
                    invalidList.append(patList[h])
                    invalidReasonList.append("Invalid Sex")
            else:
                invalidList.append(patList[h])
                invalidReasonList.append("Invalid First/Last Name")

    print(len(dumpList), "Entries In File")
    print(len(patList), "Valid Patients found")
    print(len(parentList), "Valid Parents")
    print(len(childList), "Valid Children")
    print(len(invalidList), "Invalid Entries")



filterAllPatients()





#Write all Data to File
def writeToFile():
    

    outputfilename = "preImportFilteredList.xlsx"
   
 
    combinedList = parentList
    outputdf = pd.DataFrame(columns=['Row Id', 'First', 'Last', 'Birth Day', 'Birth Month', 'Birth Year',
                                 'Patient Email', 'Guardian Email', 'Sex', "Handedness", "Start Week",
                                 "Expected Weeks", 'Username', 'Password', "Guardian FirstName",
                                 "Guardian LastName", "Note"])
    u=0
    for u in range(len(parentList)):
    
        try:
            outputdf = outputdf.append(
                {'Row Id':combinedList[u].pid, 'First':combinedList[u].fname, 
                 'Last':combinedList[u].lname, 'Birth Day':combinedList[u].bday,
                 'Birth Month':combinedList[u].bmonth, 'Birth Year':combinedList[u].byear,
                 'Guardian Email':combinedList[u].gemail,
                 'Sex':combinedList[u].sex, 'Handedness':combinedList[u].handedness,
                 'Start Week':combinedList[u].startweek,'Expected Weeks':combinedList[u].expweeks,
                 'Username':combinedList[u].username, 'Password':combinedList[u].password}
                                   ,ignore_index=True)
        except:
            print("Patient print error on line", combinedList[u].pid)


    combinedList = childList

    
    u=0
    for u in range(len(childList)):
        ### CREATE DATAFRAME FOR ALL ENTRIES 
       
        try:
            outputdf = outputdf.append(
                {'Row Id':combinedList[u].pid, 'First':combinedList[u].fname, 
                 'Last':combinedList[u].lname, 'Birth Day':combinedList[u].bday,
                 'Birth Month':combinedList[u].bmonth, 'Birth Year':combinedList[u].byear,
                 'Sex':combinedList[u].sex, 'Handedness':combinedList[u].handedness,
                 'Start Week':combinedList[u].startweek,'Expected Weeks':combinedList[u].expweeks,
                 'Username':combinedList[u].username, 'Password':combinedList[u].password,
                 'Guardian First Name':combinedList[u].guardfname, 'Guardian Last Name':combinedList[u].guardlname}
                 ,ignore_index=True)
        except:
            print("Child print error on line", u)


    combinedList = invalidList
    outputdf = outputdf.append({'Row Id':"INVALID ENTRIES BELOW"},ignore_index=True)
    u=0
    for u in range(len(invalidList)):
        try:
            outputdf = outputdf.append(
                {'Row Id':invalidList[u].pid, 'First':combinedList[u].fname, 
                 'Last':combinedList[u].lname, 'Birth Day':combinedList[u].bday,
                 'Birth Month':combinedList[u].bmonth, 'Birth Year':combinedList[u].byear,
                 'Patient Email':combinedList[u].email,
                 'Sex':combinedList[u].sex, 'Handedness':combinedList[u].handedness,
                 'Start Week':combinedList[u].startweek,'Expected Weeks':combinedList[u].expweeks,
                 'Username':combinedList[u].username, 'Password':combinedList[u].password,
                 'Guardian First Name':combinedList[u].guardfname, 'Guardian Last Name':combinedList[u].guardlname,
                 'Note':invalidReasonList[u]},ignore_index=True)
        except:
            print("invalid print error on line", u)

    
    
    writer = pd.ExcelWriter(outputfilename, engine='xlsxwriter')
    outputdf.to_excel(writer, index=False)

    writer.save()
    print("WRITE SUCCESS", outputfilename)
    

    

writeToFile()
