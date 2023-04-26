import csv
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import numpy
import sys

startdata = sys.argv[1]
number_of_games_start = int(sys.argv[1])
number_of_games_end = int(sys.argv[2])
search_categories = ['objectname', 'baverage', 'minplayers', 'maxplayers', 'playingtime','category','aweight']
parse_array = []

def loadGame(id):
  
    # url of rss feed
    url = 'https://boardgamegeek.com/xmlapi/game/' + str(id) + '&stats=1'
  
    # creating HTTP response object from given url
    try:
        resp = requests.get(url)
        # saving the xml file
        with open('xmls/bgg'+ str(number_of_games_start) + '-' + str(number_of_games_end) + '.xml', 'ab') as f:

            content = resp.content
                
            if(id != number_of_games_start):
                content = content[70:]
                
            if(id != number_of_games_end):
                content = content[:-15]
                
            #print(content)
            f.write(content)
            print("game",id,"added")
    except requests.exceptions.RequestException as e:
        print("game",id,"couldn't be added")
          
  
def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    games = tree.getroot()
  
    # create empty list for news items
    if number_of_games_start == 1:
        parse_array = [search_categories]
    else:
        parse_array = []
  
    # iterate news items
    for game in games:
        game_arr = [None] * len(search_categories)
        cat_arr = []
        for thing in game:
  
            # special checking for namespace object content:media
            if thing.tag == 'name' and 'primary' in thing.attrib and thing.attrib['primary'] == 'true':
                game_arr[0] = thing.text    
            
            if thing.tag == 'statistics':
                for stat in thing:
                    if stat.tag == 'ratings':
                        for rating in stat:
                            if(rating.tag == 'bayesaverage') and isinstance(rating.text, str):
                                game_arr[search_categories.index('baverage')] = float(rating.text)

                            if rating.tag == 'averageweight' and isinstance(thing.text, str):
                                game_arr[search_categories.index('aweight')] = float(rating.text)
                
            if thing.tag == 'minplayers' and isinstance(thing.text, str):
                game_arr[search_categories.index('minplayers')] = int(thing.text)
                
            if thing.tag == 'maxplayers' and isinstance(thing.text, str):
                game_arr[search_categories.index('maxplayers')] = int(thing.text)
                
            if thing.tag == 'playingtime' and isinstance(thing.text, str):
                game_arr[search_categories.index('playingtime')] = int(thing.text)
                
            if thing.tag == 'boardgamecategory' and isinstance(thing.text, str):
                cat_arr.append(thing.text)
                if thing.text == 'Expansion for Base-game':
                    game_arr = [None] * len(search_categories)
            
        game_arr[search_categories.index('category')] = cat_arr
        print(game_arr)
        if cat_arr and (not (None in game_arr)):
            parse_array.append(game_arr)
        # else:
        #     print(game_arr)
                
    #print('Array:',parse_array)
    print('Array length:',len(parse_array))
    return(parse_array)

      
def main():
    #clears the bgg.xml files
    bgg = open('xmls/bgg'+ str(number_of_games_start) + '-' + str(number_of_games_end) + '.xml', "w")
    bgg.close()

    # load rss from web to update existing xml file
    for n in range(number_of_games_start,number_of_games_end + 1):
        loadGame(n)

    tree = ET.parse('xmls/bgg'+ str(number_of_games_start) + '-' + str(number_of_games_end) + '.xml')
    root = tree.getroot()
    # id = int(root[0].attrib['objectid'])
    # print(hasattr(root[0][7],'primary'))
    # print('primary' in root[0][7].attrib)
    
    # parse xml file
    parse_array = parseXML('xmls/bgg'+ str(number_of_games_start) + '-' + str(number_of_games_end) + '.xml')
    
    # dataframe = pd.DataFrame(parse_array) 
    # dataframe.to_csv(r"bgg_csv.csv")
    # parse_array.tofile('bgg_csv.csv', sep = ',')
    # array = numpy.array(parse_array) 
    # numpy.savetxt("bgg_csv.csv", array, delimiter = ",")
    
    with open("bgg.csv","a",newline='') as my_csv:
        newarray = csv.writer(my_csv,delimiter=',')
        newarray.writerows(parse_array)
    
    print('parse_test successful from',number_of_games_start,'to',number_of_games_end)
    
      
if __name__ == "__main__":

    # calling main function
    main()