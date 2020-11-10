from zipfile import ZipFile
import os
import shutil
from logManager import initializeLog,lineno,writetolog,endlog

initializeLog()

loc_OTE_Tester=None		#global variable to store location of OTE_Tester since it is generated in first choice and needed in second case


def validatePath(msg):     #function to validate path of ATP,OTE and DMI and show appropriate messages
    while(True):
            writetolog(lineno()+2,"asked user to "+ msg)
            writetolog(lineno()+1,"waiting for user input")
            path=input(msg)+"\\"
            if(os.path.isdir(path)):
                writetolog(lineno(),"User entered: "+path)
                break
            else:
                writetolog(lineno(),"User entered an invalid path: "+path)
                print("Not a valid directory!!!\n")
    return path


def listZip(path):     #function to list only zip files in a given path
    writetolog(lineno(),"displayed list of files in "+ path)
    for file in os.listdir(path):
            if(file.find(".zip")!=-1):
                print(file)


while True:     #while loop where menu is implemented

    print("---------------------")
    print("       Menu")
    print("---------------------")
    print("[1] ATP")
    print("[2] OTE")
    print("[3] DMI")
    print("[4] Exit")
    print("---------------------\n")

    writetolog(lineno(),"Menu has been displayed, waiting for user to enter choice ")

    choice=input("Enter Choice:")		#variable to store choice from user

    if(choice=="1"):     #if ATP is selected
        writetolog(lineno(),"User has chosen 1: ATP")
        path_ATP=validatePath("\nEnter Location of ATP Folder:") 	#get and validate path of ATP

        print("\nFiles in ATP\n--------------")
        listZip(path_ATP)

        found=False     #flag to store whether version number is matched or not
        filename=""     #variable to store filename once version number is matched

        while(True):
            writetolog(lineno()+1,"waiting for user to enter version number")
            version=input("Enter Version number: ") 	#get version number

            for file in os.listdir(path_ATP):  #looping through filenames in given ATP path
                if(file.find("_"+version+".zip")!=-1):     #checking if file matches version number
                    path_ATP=path_ATP+file     #creating full path once version is matched
                    filename=file    	 	   #storing filename for later use
                    found=True     		       #changing flag to true since item is found
                    print("File path:",path_ATP)     #displaying full path
                    break
            if(found!=True):     #checks whether user entered a valid version number present in path or not
                writetolog(lineno(),"invalid version number entered:"+version)
                print("\nCannot find a file with version number!!!!!\nTry again")
            else:
                writetolog(lineno(),"User entered valid version number:"+version)
                break 

        dest=validatePath("Enter Destination location:")     #get and validate destination path for extraction
        old_name=dest+filename[0:-4]    	   #storing present name of extracted folder so that it can be renamed later
        loc_OTE_Tester=new_name = dest+"OTE_Tester"     	 #storing new destination file name for renaming which is same as path of OTE_Tester which is needed in Choice:2
        if(os.path.isdir(loc_OTE_Tester)):     #checks if OTE_Tester folder is already present
            writetolog(lineno(),"OTE_Tester is already present at :"+dest)
            print("\nOTE_Tester folder already present !!! \nOld one has been replaced\n")
            writetolog(lineno()+1,"Old OTE_Tester has been removed :")
            shutil.rmtree(loc_OTE_Tester)     #if OTE_Tester is already present it will be removed
        with ZipFile(path_ATP) as myzip:      #opening the zipfile
            writetolog(lineno()-1,"zipfile:"+filename+" has been opened")
            myzip.extractall(dest)     		  #extracting the zipfile
            writetolog(lineno()-11,"zipfile:"+filename+" has been extracted to: "+dest)
        os.rename(old_name,new_name)    	  #renaming present filename to OTE_Tester
        writetolog(lineno()+1,old_name+" :was renamed to: "+new_name)


    elif(choice=="2"):     #if OTE is selected
        writetolog(lineno(),"User has chosen 2:OTE")
        if(loc_OTE_Tester==None):	#if choice 1 is not run
            print("Invalid Choice \nOption [1] has to be done before option 2.Choose again !!!!\n")
        else:	#if choice 1 is ran and we have path of OTE_Teste
            path_OTE=validatePath("Enter Location of OTE Folder: ") 	#get and validate path of OTE
            print("\nFiles in OTE")
            listZip(path_OTE) 	#list zipfiles in OTE folder
            
            found=False		#flag to store whether version number is matched or not
            filename=""		#variable to store filename once version number is matched

            while(True):	#loop as long as a valid version numebr is given
                writetolog(lineno()+1,"waiting for user to enter version number")
                version=input("\nEnter Version number: ")	#get version number

                for file in os.listdir(path_OTE): 	#looping through files in OTE folder
                    if(file.find("_v"+version+".zip")!=-1):		#checks if there is a file with given version number
                        path_OTE=path_OTE+file 		#creating full path once version number is matched
                        filename=file 				#store filename for later use
                        found=True 					#change found status to true since item is found
                        print("File path:",path_OTE)
                        break
                if(found!=True):	#checks whether user entered a valid version number present in path or not
                    writetolog(lineno(),"invalid version number entered:"+version)
                    print("\nCannot find a file with version number!!!!!\nTry again")
                else:
                    writetolog(lineno(),"User entered valid version number:"+version)
                    break
                   
            with ZipFile(path_OTE) as zip_file:		#opening the zipfile
                writetolog(lineno(),"zipfile:"+filename+" has been opened")
                writetolog(lineno(),"searching for  OTEStart.exe in: "+filename)
                for member in zip_file.namelist(): 			#looping through files in zipfile since we only need OTEstart.exe
                    filename = os.path.basename(member)		#getting only file names from full path using basename() function
                    if (filename=="OTEstart.exe"):			#if OTEstart.exe is found
                        writetolog(lineno(),"OTEStart.exe has been found")
                        source = zip_file.open(member)		#open only OTEstart.exe so that contents can be copied -> this will be the source
                        target = open(os.path.join(loc_OTE_Tester, filename), "wb")		#creating destination path by joining OTE_Tester location and filename i.e, OTEstart.exe and open it in binary write mode->this will be target
                        with source, target:
                            writetolog(lineno(),"copying OTEStart.exe to OTE_Tester")
                            shutil.copyfileobj(source, target)		#copy source to target i.e, OTEstart.exe from zip to OTE_Tester folder


    elif(choice=="3"):     #if DMI is selected
        writetolog(lineno(),"User has chosen 3:DMI")
        path_DMI=validatePath("Enter Location of DMI Folder: ") 	#get and validate path of DMI
        print("\nFiles in DMI")
        listZip(path_DMI)	#list zipfiles in DMI

        found=False		#flag to store whether version number is matched or not
        
        while(True):

            filename=""		#variable to store filename once version number is matched
            writetolog(lineno()+1,"waiting for user to enter version number")
            version=input("\nEnter version number: ")	#get version number
            for file in os.listdir(path_DMI):	#looping through filenames in given DMI path
                if(file.find("_"+version+".zip")!=-1):	#checks if there is a file with given version number
                    path_DMI=path_DMI+file 		#creating full path once version number is matched
                    filename=file 				#store filename for later use
                    found=True 					#change found status to true since item is found
                    print("File path:",path_DMI)
                    break

            if(found!=True):	#checks whether user entered a valid version number present in path or not
                writetolog(lineno(),"invalid version number entered:"+version)
                writetolog(lineno()+1,"cannot find:"+filename)
                print("\nCannot find a file with version number!!!!!\nTry again")
            else:
                writetolog(lineno(),"User entered valid version number:"+version)
                break

        while(True):
            path_dest=validatePath("Enter destination location:")+"DMIApp"			#get and validate destination path and append DMIApp to path
            replaceDMI=None		#varibale for storing whether to replace DMIApp folder
            if(os.path.isdir(path_dest)):	#if DMIApp already exists
                writetolog(lineno(),"DMIApp folder already present at destination")
                while(True):
                    replaceDMI=input("DMIApp folder already exist in the directory , Do you want to replace it(Y/N):")		#asking user whether or not to replace DMIApp folder
                    if(replaceDMI in ["Y","y","N","n"]):	#check if user gave a valid input
                        break
                    else:
                        print("Invalid choice!!!")
                if(replaceDMI in ["Y","y"]):	#if user wants to replace DMIApp
                    writetolog(lineno(),"User chose to replace the folder")
                    shutil.rmtree(path_dest)	#remove existing DMIApp and its contents
                    writetolog(lineno(),"Old DMIApp at destination has been deleted :"+path_dest)
                    break
            else:
                break
        
        os.mkdir(path_dest)		#create new DMIApp folder in destination
        writetolog(lineno()-1,"New folder named DMIApp created :"+path_dest)
        old_name=path_dest +"\\"+filename[0:-4]		#storing present name of extracted folder so that it can be renamed later

        DMI_A=path_dest+"\\DMIAppA"		#creating path of DMIAppA folder
        DMI_B=path_dest+"\\DMIAppB"		#creating path of DMIAppB folder
        print("path_dest:",path_dest)

        with ZipFile(path_DMI) as zip_file:		#open zipfile
            writetolog(lineno(),"Zipfile: "+filename +" opened")
            zip_file.extractall(path_dest)	    #extract all files in zip to destination path
            writetolog(lineno(),"Zipfile: "+filename +" has been extracted to "+path_dest)
            os.rename(old_name,DMI_A)		    #rename from extracted folder name to DMIAppA
            writetolog(lineno(),"renamed: "+old_name+": to :"+DMI_A)
            zip_file.extractall(path_dest)	    #extract all files in zip to destination path		
            writetolog(lineno(),"Zipfile: "+filename +" has been extracted to "+path_dest)
            os.rename(old_name,DMI_B)		    #rename from extracted folder name to DMIAppB
            writetolog(lineno(),"renamed: "+old_name+": to :"+DMI_B)

    elif(choice=="4"):     #Exit Main Menu loop/application
        writetolog(lineno(),"User has chosen 4:Exiting application")
        break;

    else: 					#Handling exception case
        writetolog(lineno(),"User has entered an invalid choice")
        print("\nInvalid Choice!!!!!!!!!\n")

endlog()
        