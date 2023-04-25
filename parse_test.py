import csv
import requests
import xml.etree.ElementTree as ET

number_of_games = 10
search_categories = ['objectname', 'baverage', 'minplayers', 'maxplayers', 'playingtime']

def loadGame(id):
  
    # url of rss feed
    url = 'https://boardgamegeek.com/xmlapi/game/' + str(id)
  
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
        
    with open('bgg2.xml', 'wb') as f:
        
        content = resp.content
        f.write(content)
          
  
def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    games = tree.getroot()
  
    # create empty list for news items
    csv_array = [search_categories]
  
    # iterate news items
    for game in games:
        game_arr = [None] * len(search_categories)
        for thing in game:
  
            # special checking for namespace object content:media
            if thing.tag == 'name' and 'primary' in thing.attrib and thing.attrib['primary'] == 'true':
                game_arr[0] = thing.text
                
        if True:
            csv_array.append(game_arr)
                
    print(csv_array)

      
def main():
    #clears the bgg.xml files
    bgg = open("bgg.xml", "w")
    bgg.close()

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
    parseXML('bgg.xml')
    
      
if __name__ == "__main__":

    # calling main function
    main()