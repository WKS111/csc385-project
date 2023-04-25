import csv
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import numpy

number_of_games = 100
search_categories = ['objectname', 'baverage', 'minplayers', 'maxplayers', 'playingtime']
parse_array = []

def loadGame(id):
  
    # url of rss feed
    url = 'https://boardgamegeek.com/xmlapi/game/' + str(id) + '&stats=1'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open('bgg.xml', 'ab') as f:
        
        content = resp.content
        
        if(id != 1):
            content = content[70:]
        
        if(id != number_of_games):
            content = content[:-15]
            
        #print(content)
        f.write(content)
        
    with open('bgg2.xml', 'ab') as f:
        
        content = resp.content
        f.write(content)
          
  
def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    games = tree.getroot()
  
    # create empty list for news items
    parse_array = [search_categories]
  
    # iterate news items
    for game in games:
        game_arr = [None] * len(search_categories)
        for thing in game:
  
            # special checking for namespace object content:media
            if thing.tag == 'name' and 'primary' in thing.attrib and thing.attrib['primary'] == 'true':
                game_arr[0] = thing.text    
            
            if thing.tag == 'statistics':
                for stat in thing:
                    if stat.tag == 'ratings':
                        for rating in stat:
                            if(rating.tag == 'bayesaverage'):
                                game_arr[search_categories.index('baverage')] = float(rating.text)
                
            if thing.tag == 'minplayers':
                game_arr[search_categories.index('minplayers')] = int(thing.text)
                
            if thing.tag == 'maxplayers':
                game_arr[search_categories.index('maxplayers')] = int(thing.text)
                
            if thing.tag == 'playingtime':
                game_arr[search_categories.index('playingtime')] = int(thing.text)
            
        if not (None in game_arr):
            parse_array.append(game_arr)
        else:
            print(game_arr)
                
    #print('Array:',parse_array)
    print('Array length:',len(parse_array))
    return(parse_array)

      
def main():
    #clears the bgg.xml files
    bgg = open("bgg.xml", "w")
    bgg.close()
    bgg2 = open("bgg2.xml", "w")
    bgg2.close()

    # load rss from web to update existing xml file
    for n in range(1,number_of_games + 1):
        loadGame(n)
        print('Game',n,'added')
  
    tree = ET.parse('bgg.xml')
    root = tree.getroot()
    # id = int(root[0].attrib['objectid'])
    # print(hasattr(root[0][7],'primary'))
    # print('primary' in root[0][7].attrib)
    
    # parse xml file
    parse_array = parseXML('bgg.xml')
    
    # dataframe = pd.DataFrame(parse_array) 
    # dataframe.to_csv(r"bgg_csv.csv")
    # parse_array.tofile('bgg_csv.csv', sep = ',')
    # array = numpy.array(parse_array) 
    # numpy.savetxt("bgg_csv.csv", array, delimiter = ",")
    
    with open("bgg.csv","w",newline='') as my_csv:
        newarray = csv.writer(my_csv,delimiter=',')
        newarray.writerows(parse_array)
    
    
      
if __name__ == "__main__":

    # calling main function
    main()