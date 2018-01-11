import requests 
import json
import sys


def doubleDigit(num):
    if num < 10 :
        return '0'+str(num)
    else:
        return str(num)


def main(v_id,c_id):
    
        
    if sys.version_info[0] == 2:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    
    videoId = v_id
    clientId = c_id
    
    

    chat = []
    time = []
    user = []
    
    nextCursor = ''
    
    params = {}
    params['client_id'] = clientId
    
    
    i = 0
    
    while True :
        if i == 0 :
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?content_offset_seconds=0' 
            i += 1
        else:
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?cursor=' 
            URL +=  nextCursor   
            
       
        
        response = requests.get(URL, params=params)
        
        j = json.loads(response.text)
        
        for k in range(0,len(j["comments"])):
            timer = j["comments"][k]["content_offset_seconds"]
            
            timeMinute = int(timer/60)
            
            if timeMinute >= 60 :
                timeHour = int(timeMinute/60)
                timeMinute %= 60
            else :
                timeHour = int(timeMinute/60)
    
            timeSec = int(timer%60)
            
            time.append(doubleDigit(timeHour)+':'+doubleDigit(timeMinute)+':'+doubleDigit(timeSec))
            user.append(j["comments"][k]["commenter"]["display_name"])
            chat.append(j["comments"][k]["message"]["body"])
       
        if '_next' not in j:
            break
        
        nextCursor = j["_next"]
            
    
    f = open(videoId+".txt", 'wt')
    
    for x in range(0, len(time)): 
            f.write('[')
            f.write(str(time[x]))
            f.write(']')
            f.write(' ')
            f.write('<')
            f.write(str(user[x]))
            f.write('>')
            f.write(' ')
            f.write(str(chat[x]))
            f.write("\n")
            
    f.close()
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])