from time import sleep
import datetime
import os
import asyncio

import requests as req;
import csv

# from selenium import webdriver;
# from bs4 import BeautifulSoup;
# import pandas as pd;

# driver = webdriver.Chrome("./chromedriver");

def geDataRouletteRecent() -> object:
  blazeRequest = req.get("https://blaze.com/api/roulette_games/recent");

  dataRoulette = blazeRequest.json(); 
  
  return dataRoulette;

async def writeCsv(path: str, args: list): 
  f = open(path, 'a')

  try: 
    csv.writer(f, delimiter=",").writerow(args)
    f.close()

    return 

  except Exception as err:
    print("Error writing", err)

async def readCsv(path: str) -> list: 
  f = open(path, 'r')

  try: 
    r_file = list(csv.DictReader(open(path, "r")))
    f.close()

    return r_file;

  except Exception as err:
    print("Error writing", err)

def compareDatetime(startDatetime: datetime, endDatetime: str) -> datetime.timedelta: 
  data = endDatetime.split("T");

  data[0] = data[0].split("-")
  data[1] = data[1].split(":")

  data[1][2] = data[1][2].replace("Z", "").split(".")[0]

  count_x = 0
  for t in data:
    count_y = 0
    for i in data[count_x]:
      data[count_x][count_y] = int(i)
      count_y += 1

    count_x += 1

  formatEndDate = datetime.datetime(int(data[0][0]),data[0][1],data[0][2],data[1][0],data[1][1],data[1][2])

  return startDatetime - formatEndDate;


  




if __name__ == "__main__":
  path_db = "./database.csv"

  async def writeAllOccurrences(): 
    roulette = geDataRouletteRecent()[::-1];

    for i in roulette:
      writeCsv(path_db,[i["id"], i["color"], i["created_at"], i["roll"]])

  async def run():
    read_db = await readCsv(path_db)

    total_rows = len(read_db);

    print(read_db)

    if total_rows == 0:
        await writeCsv()
        
    print(total_rows, total_rows == 0)

    if total_rows >= 20:
      secondsDiff = compareDatetime(datetime.datetime.utcnow(), read_db[total_rows - 1]['created_at']).seconds


      if secondsDiff > 600:
        print("entrou")

        writeAllOccurrences()

        print("end")
        
      await asyncio.sleep(1)
    # while True:

    #   # if os.path.getsize("./database.csv") < 0:
    #   #   for data in dataRoulette:
    #   #       csv.writer(database, delimiter=",").writerow([data["id"], data["color"], data["created_at"], data["roll"]])

      
    #   sleep(30.0)


asyncio.run(run())