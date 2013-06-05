import json

class GlobalComment():
    def __init__ (self):
        self.comment = self.getComment()

    def getComment (self):
        if 'comment' in self.data:
            return self.data['comment']
        else:
            return None


class HAR(GlobalComment):
    def __init__(self, inputFile=None, string=None):
        #eventually add args / kwargs for file/string input
        if inputFile is not None:
            inputFile.open()
            interpreted_dict = json.load(inputFile)
            inputFile.close()
        elif string is not None:
            interpreted_dict = json.loads(string)
        else:
            raise Exception("No input provided!")
        self.data = interpreted_dict['log']
        self.creator = self.getCreator()
        self.browser = self.getBrowser()
        self.version = self.getVersion()
        if 'entries' in self.data:
            self.entries = []
            for item in self.data['entries']:
                self.entries.append(Entry(item))
        else:
            self.entries = None

        if 'pages' in self.data:
            self.pages = []
            for item in self.data['pages']:
                self.pages.append(Page(item))
        else:
            self.pages = None #pages are optional, so this is 


    def getBrowser (self): #browser is optional, return null if not present
        try:
            return self.data['browser']
        except:
            return None

    def getCreator (self):
        try:
            return self.data['creator']
        except:
            return None

    def getVersion (self):
        try:
            version = self.data['version']
            if not len(version) > 0:
                raise TypeError
            else:
                return version
        except:
            return "1.1" #1.1 is assumed by default, as per the .HAR file spec

    def getMatchedEntries (self, matchString):
        """
        For a given matchString that varies by vendor (e.g. /b/ss for Omniture) yield back request objects and time requests
        
        Disregard all entries that aren't HTTP Status == 200, because those aren't real, at least for Omniture.
        """
        entries = self.data['log']['entries']
        for entry in entries:
            request = entry['request']
            response = entry['response']
            startTime = entry['startedDateTime'] #in ISO 8601
            if matchString in request['url']: # and (response['status'] is 200 or response['status'] is 302): #look for the matchstring, also check that the status is OK
                #import pdb;pdb.set_trace()
                yield request, startTime
                
            
    def getDictFromListofDicts (self, request):
        stuff = {}
        for item in request['headers']:
            stuff[item['name']] = item['value']
        return stuff


class Entry(GlobalComment):
    #do something
    def __init__(self, data):
        pass



class Page(GlobalComment):
    #do something
    def __init__(self):
        pass