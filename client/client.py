#!/usr/bin/env python3
'''
Script for client side
@author: hao
@co-author: Wilkenson
'''
import config   
import protocol
from socket import *
import os

class client:
    
    fileList=[] # list to store the file information 
    uploadList=[]

    #Constructor: load client configuration from config file
    def __init__(self):
        self.serverName, self.serverPort, self.clientPort, self.downloadPath, self.uploadPath = config.config().readClientConfig()
        # print("Server Name:",self.serverName)
        # print("Download Path:",self.downloadPath)
        # print("Upload Path:",self.uploadPath)

    # Function to produce user menu 
    def printMenu(self):
        print("Welcome to simple file sharing system!")
        print("Please select operations from menu")
        print("--------------------------------------")
        print("1. Review the List of Available Files to Download")
        print("2. Download File")
        # *******************************
        # ADD one line here for uploading files
        print("3. Review the List of Available Files to Upload")
        print("4. Upload File")
        
        print("5. Quit")

    # Function to get user selection from the menu
    def getUserSelection(self):       
        ans=0
        # only accept option 1-3
        # ******************************
        # When you add upload option, you need to modify the number of options
        # you accept
        while ans>5 or ans<1:
            self.printMenu()
            try: 
                ans=int(input("\nChoose an option: "))
            except:
                ans=0
            if (ans<=5) and (ans>=1):
                return ans
            print("Invalid Option")

    # Build connection to server
    def connect(self):
        serverName = self.serverName
        serverPort = self.serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        return clientSocket 
    

    # Get file list from server by sending the request
    def getFileList(self):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_REQUEST," "))
        header, msg=protocol.decodeMsg(mySocket.recv(1024).decode())
        mySocket.close()
        if(header==protocol.HEAD_LIST): 
            files=msg.split(",")
            self.fileList=[]
            for f in files:
                self.fileList.append(f)
        else:
            print ("Error: cannot get file list!")

    # function to print files in the list with the file number
    def printFileList(self):
        count=0
        for f in self.fileList:
            count+=1
            print('{:<3d}{}'.format(count,f))
        print()

    # Function to select the file from file list by file number,
    # return the file name user selected
    def selectDownloadFile(self):
        if(len(self.fileList)==0):
            self.getFileList()
        ans=-1
        print()
        while ans<0 or ans>len(self.fileList)+1:
            self.printFileList() 
            try:
                print("Please select the file you want to download from the list (enter the number of files):")
                ans=int(input("File Number: "))
                print()
            except:
                ans=-1
            if (ans>0) and (ans<len(self.fileList)+1):
                return self.fileList[ans-1]
            print("Invalid number")

    # Function to send download request to server and wait for file data
    def downloadFile(self,fileName):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_DOWNLOAD, fileName))
        with open(self.downloadPath+"/"+fileName, 'wb') as f:
            print("\ndownloaded from server") 
            while True:
                #print('receiving data...')
                data = mySocket.recv(1024)
                #print('data=%s', (data))
                if not data:
                    break
            # write data to a file
                f.write(data)
        print(fileName+" has been downloaded!\n")
        mySocket.close()

    #********************************************
    # Please complete the upLoadFile function, the function takes a file name as
    # an input
    def upLoadFile(self,fileName): 
         
        try:  
            s_socket = self.connect()  
            s_socket.send(protocol.prepareMsg(protocol.HEAD_UPLOAD, fileName))

            with open(self.downloadPath+"/"+fileName, 'rb') as f: 
                print("\nUploading file to server")
                data = f.read(1024)
                while data:
                    s_socket.send(data)
                    data = f.read(1024) 
                print(fileName+" has been uploaded\n")
            s_socket.close()

        except FileNotFoundError as e:
            print("File not found [" + str(e) + "]\n")
        

    
    def getUploadList(self): 
        self.uploadList = os.listdir(self.downloadPath) 
        return self.uploadList
    
    # function to print files in the list with the file number
    def printUploadList(self):
        count=0
        # print("Download Path:",self.downloadPath)
        self.uploadList = self.getUploadList()
        if not self.uploadList:
            print("No files to upload!")
        else:
            for u in self.uploadList:
                count += 1
                print('{:<3d}{}'.format(count,u))

    #********************************************
    # Please complete the select Upload file function,
    # The function should print out a list of files from upload folder for user to
    # select, and user need to chose one file.
    # The return value should be a file name

    def selectUploadFile(self):
      
        upload_list_length = len(self.uploadList)\
        if self.uploadList else len(self.getUploadList()) 

        ans = -1
            
        while ans < 0 or ans > upload_list_length + 1:
            self.printUploadList()
            try:
                print("\nPlease select the file you want to upload from the list (enter the number of files):") 
                ans=int(input("File Number : "))
                print()

                if ans > 0 and ans < (upload_list_length + 1): 
                    return self.uploadList[ans-1] 
            except:
                ans = -1
                print("Invalid number")
            
 
        
    # Main logic of the client, start the client application
    def start(self):
        opt=0
        while opt!=5:
            opt=self.getUserSelection()
            if opt==1:
                if(len(self.fileList)==0):
                    self.getFileList()
                self.printFileList()                  
            elif opt==2:
                self.downloadFile(self.selectDownloadFile())
            elif opt==3:
                self.printUploadList()
            elif opt==4:
                self.upLoadFile(self.selectUploadFile())
                 


            #**************************
            # You need another option for uploading files
            else:
                pass
                
def main():
    c=client() 
    c.start()
main()
