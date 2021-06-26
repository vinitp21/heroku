
import json
import os
import random
import traceback
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
import math
from datetime import date,datetime,timedelta


from flask import Flask

from flask import request, make_response

app = Flask(__name__)        

@app.route('/')
@app.route('/Home')
def Home():
    return "Hello"
global name,Emailsend,OTP,emailUP




# function displaying the text on facebook
def make_text_response(message, platform="FACEBOOK"):
    return {
        "text": {
            "text": [
                message,
            ]
        },
        "platform": platform
    }


def show(information, information_previous):
    global information_sample
    if len(information) != 0:
        information_sample = random.choice(information)
        information_previous.append(information_sample)
        information.remove(information_sample)
    return information_sample
    


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = process_request(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def process_request(req):

    global name, email, reasn,empid,Emailsend,OTP,emailUP
    global Dept

    try:
       
        action = req.get("queryResult").get("action")

        if action == "input.welcome":

            return {
                "source": "webhook"
            }

        if action == "emp_id":
           result = req.get("queryResult").get("queryText")
           empid = result
           print(empid)   
           
           cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
           db = cluster["employee_name"]
           collection = db["employee"] 
           results = collection.find_one({"_id":empid})
           print(results)
           if (results)==None:
            print("Please provide correct employee id")  
            return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Invalid employee id\nPlease type the correct employee id"
                            ]
                        },
                        
                        "platform": "SLACK"
                    }
                ],
                            "outputContexts": [
                {
                    "name": "projects/formidable-deck-310515/agent/sesions/def406c3-fa02-085e-0a2d-7d17a766b7e6/contexts/welcome_intent2",
                    "lifespanCount": 1
                }
                ]
            }
           else:
                i = results.values()
                x = list(i)
                print(x[0])
                print("Thankyou for validation")
                Emailsend = x[4]     
                print(Emailsend)
                name = x[1]


        #    global OTP
           digits = "0123456789"
           OTP = ""

           for i in range(4):
               OTP += digits[math.floor(random.random() * 10)]
               print(OTP)
           cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
           db = cluster["employee_name"]
           collection = db["employee"] 
           results = collection.update_one({"_id": empid},{"$set":{"OTP": OTP}})
           print(results)    
           
           

           sender_addres = 'son.pari2314@gmail.com'
           sender_pas = 'Vinit@123'
            

           reciver_mail = Emailsend

           print(reciver_mail)

           mesage = MIMEMultipart()
           mesage['From'] = sender_addres
           mesage['To'] = reciver_mail
           mesage['Subject'] = 'Mail using python'
           text = " "
           html = """\
                <html>
                    <head></head>
                    <body>
                    <p>Hi {}, your OTP for verification is {} <br>
                        <br>
                            
                        <br>
                            Regards,<br>
                            Morphi <br>
                            HR asistant
                    </p>
                    </body>
                </html>
                """.format(name, OTP)
           mesage.attach(MIMEText(text, 'plain'))
           mesage.attach(MIMEText(html, 'html'))
           s = smtplib.SMTP('smtp.gmail.com', 587)
           s.starttls()
           s.login(sender_addres, sender_pas)
           text = mesage.as_string()
           s.sendmail(sender_addres, reciver_mail, text)
           s.quit()
           print('Mail Sent')

        if action =="OTP_verify":
           result = req.get("queryResult").get("queryText")
           OTP_verify = result
           print(OTP_verify)
           cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
           db = cluster["employee_name"]
           collection = db["employee"] 
           results = collection.find_one({"_id": empid})
           print(results)
           i = results.values()
           x = list(i)
           OTP_cnf = x[6]
           print(OTP_cnf)
           if OTP==OTP_verify:
               print("Thankyou") 
           else:
               return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Invalid OTP, Please enter the correct one"
                            ]
                        },
                        
                        "platform": "SLACK"
                    }
                ],
                            "outputContexts": [
                {
                    "name": "projects/formidable-deck-310515/agent/sesions/def406c3-fa02-085e-0a2d-7d17a766b7e6/contexts/Otp_Verify",
                    "lifespanCount": 1
                }
                ]
            }
            
        if action == "reasonAL":
            result = req.get("queryResult").get("queryText")
            reasn = result
            print(reasn)   
            
            
            global li, lt
            sender_addres = 'son.pari2314@gmail.com'
            sender_pas = 'Vinit@123'
            

            reciver_mail = "vinitpatil874@gmail.com"

            print(reciver_mail)

            mesage = MIMEMultipart()
            mesage['From'] = sender_addres
            mesage['To'] = reciver_mail
            mesage['Subject'] = 'Mail using python'
            text = " "
            html = """\
                    <html>
                        <head></head>
                        <body>
                        <p>Please refer the details below for leave application <br>
                            <br>
                                Name : {}<br>
                                Email : {} <br>
                                Reason : {}<br>
                            <br>
                                Regards,<br>
                                Morphi <br>
                                HR asistant
                        </p>
                        </body>
                    </html>
                    """.format(name, Emailsend, reasn)
            mesage.attach(MIMEText(text, 'plain'))
            mesage.attach(MIMEText(html, 'html'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_addres, sender_pas)
            text = mesage.as_string()
            s.sendmail(sender_addres, reciver_mail, text)
            s.quit()
            print('Mail Sent')
            cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = cluster["employee_name"]
            collection = db["employee"] 
            results = collection.update_one({"_id": empid},{"$inc":{"Number of leave": 1
             }})
            print(results)
        
        
            
        if action=="ask_emailUP":
           result = req.get("queryResult").get("queryText")
           regex = '[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'
           if (re.match(regex, result)):
               emailUP = result
               print(emailUP)
           else:
                return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Invalid email\nPlease type the correct email addres"
                            ]
                        },
                        "platform": "SLACK"
                    }
                ],  
                     "outputContexts": [
                    {
                        "name": "projects/formidable-deck-310515/agent/sesions/def406c3-fa02-085e-0a2d-7d17a766b7e6/contexts/update_email",
                        "lifespanCount": 1,
                        
                    }
                    ]
                  }    
          
           cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
           db = cluster["employee_name"]
           collection = db["employee"] 
           results = collection.update_one({"_id": empid},{"$set":{"Email": emailUP}})
           print(results)

        if action=="ask_contactUP":
            result = req.get("queryResult").get("queryText")
            contactUP = result
            print(contactUP)
            cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = cluster["employee_name"]
            collection = db["employee"] 
            results = collection.update_one({"_id":empid},{"$set":{"Contact No": int(contactUP)}})
            print(results)   
        global NameofFeedback
        if action=="N_feedback":
           result = req.get("queryResult").get("queryText")
           NameofFeedback = result
           print(NameofFeedback)
        
        global ReasonofFeedback
        if action=="Rsn_feedback":
           result = req.get("queryResult").get("queryText")
           ReasonofFeedback = result
           print(ReasonofFeedback)  
        if action=="ask_holiday":
            today = date.today()
            today1 = str(today)
            datetimeobject = datetime.strptime(today1,'%Y-%m-%d')
            newformat = datetimeobject.strftime('%m%d%Y')
            print(newformat)

            cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = cluster["employee_name"]
            collection = db["holiday"]
            results = collection.find_one({"Date":newformat})
            # for result in results:
            print(results)
            if (results)==None:
                print("Today is working day")
                return {
                    "source": "webhook",
                    "fulfillmentMesages": [
                        {
                            "text": {
                                "text": [
                                    "Today is a working day"
                                ]
                            },
                            "platform": "SLACK"
                        }
                    ]
                }
            else:
                i = results.values()
                x = list(i)
                holiday = x[1]
                print("Yes, today is holiday on the account of",holiday)   
                return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Yes, today is holiday on the account of {}".format(holiday)
                            ]
                        },
                        "platform": "SLACK"
                    }
                ]
                } 
        if action=="ask_holiday_tomorrow":
           presentday = date.today() 
           tomorrow = presentday + timedelta(1)
           tomorrow1 = str(tomorrow)
           datetimeobject = datetime.strptime(tomorrow1,'%Y-%m-%d')
           newformat = datetimeobject.strftime('%m%d%Y')
           print(newformat)
           cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
           db = cluster["employee_name"]
           collection = db["holiday"]
           results = collection.find_one({"Date":newformat})
            # for result in results:
           print(results)
           if (results)==None:
                print("To is working day")
                return {
                    "source": "webhook",
                    "fulfillmentMesages": [
                        {
                            "text": {
                                "text": [
                                    "Tomorrow is a working day"
                                ]
                            },
                            "platform": "SLACK"
                        }
                    ]
                }
           else:
                i = results.values()
                x = list(i)
                holiday = x[1]
                print("Yes, today is holiday on the account of",holiday)   
                return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Yes, tomorrow is holiday on the account of {}".format(holiday)
                            ]
                        },
                        "platform": "SLACK"
                    }
                ]
                } 

        if action == "name_emp" :
           result = req.get("queryResult").get("queryText")
           emp_name = result 
           print(emp_name)
           cluster = MongoClient("mongodb+srv://testing:Vinit123@cluster0.y9z3u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
           db = cluster["employee_name"]
           collection = db["employee"] 
           results = collection.find({'Name': { '$regex': emp_name, '$options': 'i' }})
           nam = list(results)
           var =  bool(nam)
           if var==True:
            for result in nam:
             print(result)
            
            print("yes")
            i = result.values()
            x = list(i)
            empname = x[1]
            contactemp = x[3]
            emailemp = x[4]
            designationemp = x[5]
            return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Employee name: {}\n  Contact: {}\n  Email: {}\n  Designation: {}".format(empname,contactemp,emailemp,designationemp)
                                  
                            ]
                        },
                        "platform": "SLACK"
                    }
                ]
                } 
           else:
            print("no") 
            return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "There is no employee with name {}. Please enter valid employee name".format(emp_name)
                                  
                            ]
                        },
                        "platform": "SLACK"
                    }
                ]
                } 
        if action == "up_holiday":
            presentday = date.today() 
            tomorrow = presentday + timedelta(1)
            tomorrow1 = str(tomorrow)
            datetimeobject = datetime.strptime(tomorrow1,'%Y-%m-%d')
            newformat = datetimeobject.strftime('%m%d%Y')
            print(newformat)

            holiday = {"01262021":"Republic Day","03292021":"Holi","04212021":"Ram Navami","05262021 ":"Bhuddha Purnima","07212021":"Id-Ul-Zuha","08302021":"Janmashtami","10152021":"Dusehra","11192021":"Diwali","12242021":"Christmas Break"}
            values = holiday.values()
            print(values)
            keys = holiday.keys()
            keys_list = list(keys)
            values_list = list(values)
            print(keys)

            for i in range(len(keys_list)):
             if newformat < keys_list[i]:
              s = str(keys_list[i])
              if s[0:2]=="01":
                  print("January")
              elif s[0:2]=="03":
                  print("January")
              elif s[0:2]=="07":
                   A = "July" 
              elif s[0:2]=="01":
                  print("April") 
              elif s[0:2]=="01":
                  print("January") 
              elif s[0:2]=="01":
                  print("January") 
              elif s[0:2]=="01":
                  print("January") 
              elif s[0:2]=="01":
                  print("January") 
              elif s[0:2]=="01":
                  print("January") 
              elif s[0:2]=="01":
                  print("January") 
              elif s[0:2]=="01":
                  print("January") 
              D = A + "/" + s[2:4] + "/" + s[4:8]
                       
              print("Next holiday is on {} on account of {}".format(D,values_list[i]))
              break
            return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Next holiday is on {} on account of {}".format(D,values_list[i])
                                
                            ]
                        },
                        "platform": "SLACK"
                    }
                ]
            }
        Dept = ""     
        if action == "Department":
           Dept = req.get("queryResult").get("queryText")
           print(Dept)   


        if action == "Raise":
            result = req.get("queryResult").get("queryText")
            Raise = result
            print(Raise)   
            print(Dept)
            
            global li, lt
            sender_addres = 'son.pari2314@gmail.com'
            sender_pas = 'Vinit@123'
            

            reciver_mail = "vinitpatil874@gmail.com"

            print(reciver_mail)

            mesage = MIMEMultipart()
            mesage['From'] = sender_addres
            mesage['To'] = reciver_mail
            mesage['Subject'] = 'Mail using python'
            text = " "
            html = """\
                    <html>
                        <head></head>
                        <body>
                        <p>Please refer the details below for leave application <br>
                            <br>
                                Depart : {}<br>
                                Reason : {}<br>
                            <br>
                                Regards,<br>
                                Morphi <br>
                                HR asistant
                        </p>
                        </body>
                    </html>
                    """.format(Dept,Raise)
            mesage.attach(MIMEText(text, 'plain'))
            mesage.attach(MIMEText(html, 'html'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_addres, sender_pas)
            text = mesage.as_string()
            s.sendmail(sender_addres, reciver_mail, text)
            s.quit()
            print('Mail Sent')             



    # if some error occure then display this mesage
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return {
                "source": "webhook",
                "fulfillmentMesages": [
                    {
                        "text": {
                            "text": [
                                "Hey your verification is pending, please verify yourself to proceed further"
                                  
                            ]
                        },
                        "platform": "SLACK"
                    }
                ]
                } 
        

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {}".format(port))
    app.run(debug=True, port=port, host='127.0.0.1')

