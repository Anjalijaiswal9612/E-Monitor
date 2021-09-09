#from pydrive.drive import GoogleDrive 
#from pydrive.auth import GoogleAuth 
import pyscreenshot, requests, pprint, json
import time 
from base64 import b64encode
import os, datetime
from PIL import ImageGrab

class support():
    def __init__(self, Eid):
        self.Eid = Eid
        
    # def connectGD(self):
    #     self.gauth = GoogleAuth() 
    #     self.gauth.LocalWebserverAuth()        
    #     self.drive = GoogleDrive(self.gauth) 
    
    # def uploadInDrive(self, path):
    #     print(path)
    #     folder_name = 'Sir'  # Please set the folder name.
    #     folders = self.drive.ListFile({'q': "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    #     # Find the destination folder
    #     for folder in folders:
    #         if folder['title'] == folder_name:
    #             Folder = folder
    #     # Upload files in the folder
    #     for x in os.listdir(path):
    #         file2 = self.drive.CreateFile({'title': x,'parents': [{'id': Folder['id']}]})
    #         file2.SetContentFile(os.path.join(path, x))
    #         file2.Upload()         
    #         f = None

    def takeScreenshot(self):
        timestamp = datetime.datetime.now().strftime("%Hhr.%Mmin [%d_%b_%Y]")
        imgName =  self.Eid+"_"+ timestamp
        
        path = os.getcwd()+ "\\Resourses\\Upload"
        
#        if(os.path.isFile(path)):
#            os.mkdir(path)
#            path = path + "\\Upload"
#            if(os.path.isFile(path)):
#            os.mkdir(path)
#        except OSError:
#            try:
#                path = path + "\\Upload" 
#                os.mkdir(path)                    
        
        name = path +"\\"+ imgName + " .png"
        if(os.name == 'posix'): # se for unix-like
            img = pyscreenshot.grab()
            img.save(name)
        elif(os.name == 'nt'): # se for windows
            img = ImageGrab.grab()
            img.save(name)
        time.sleep(1)
        pushToServer(name)
        os.remove(name) 


def pushToServer(path):
    img = None
    print("Phusing image to server")
    
    with open(  path, 'rb') as image:
        img = b64encode(image.read())
    
    data = {
        "eid":eid,
        "path":cappath,
        "escimg":img
        }
    try:
        response = requests.post(url="http://"+capurl, data=data)
        pprint.pprint(response)
    except Exception:
        print("network error")

def Authenticate(eID, cID):
    API_ENDPOINT = " https://www.emonitor.cbascorp.com/api/comp/empcheck"

    data = {
        "copid":cID,
        "eid":eID
    }

    # sending post request and saving response as response object
    print("sending") 
    r = requests.post(url = API_ENDPOINT, data = data) 
    print(r)
    # extracting response text  
    try:
        res = json.loads(r.text) 
        global captime, capurl, cappath, eid
        eid = data['eid']
        captime = res[0]['captime']
        capurl = res[0]['capurl']
        cappath = res[0]['cappath']
        print("printing responce for authentication")
        pprint.pprint(res)
        return [True, captime] 
    except Exception as e:
        print(e)
        print("Authentication failed")
        return [False]

# Authenticate("c5747", "cbascorpe100")
