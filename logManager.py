import datetime
import inspect

def lineno():	#function to get current line number
    return inspect.currentframe().f_back.f_lineno

now = datetime.datetime.now()	#get current time stamp
logname="Log_"+ now.strftime("%d_%m_%Y_%H-%M-%S") +".log"	#create a log file name using timestamp

def initializeLog():	#function to create and initialize log file with start time and column names
    file=open(logname,"w")
    file.write("Start time: "+now.strftime("%d/%m/%Y_%H:%M:%S")+"\n\n")
    file.write("{:<20}{:<30}{:<20}{:<40}\n".format("Serial Number","Timestamp","Line number","Event"))
    file.close()


def writetolog(line,msg):	#function to add a new entry to log
    writetolog.counter += 1
    file=open(logname,"a")
    file.write("{:<20}{:<30}{:<20}{:<40}\n".format(writetolog.counter,now.strftime("%d/%m/%Y_%H:%M:%S"),line,msg))
    file.close()
writetolog.counter = 0

def endlog():	#function to add end time and close the log file after the application had a successful run
    file=open(logname,"a")
    file=open(logname,"a")
    file.write("\n\nThe program ran successfully with no error\n\n")
    file.write("End Time: "+now.strftime("%d/%m/%Y_%H:%M:%S"))
    file.close()



