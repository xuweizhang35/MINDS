import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import timedelta, date
import datetime

# author: Xuwei Zhang

class orbital:
    def __init__(self):
        self.start_url = 'https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches'

    def daterange(self,start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def get_res(self, start_url):
        response = requests.get(start_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        data = soup.select('#mw-content-text > div > table:nth-child(20) > tbody')

        row = 0
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        launch_dic = {}

        for item in data[0]:
            if len(item) != 1 and len(item) != 2:

                # single launch
                if len(item) == 10 and row != 0:
                    success = 0
                    exist = 0

                    time_draft = item.text.split('[')[0]

                    dd = int(time_draft.split(" ")[0].replace("\n", ""))
                    mm = months.index("".join(re.split("[^a-zA-Z]*", time_draft.split(" ")[1]))) + 1

                    launch_date = datetime.datetime(2019, mm, dd, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)

                # payloads
                if len(item) == 12 and row != 2:
                    if ('Operational' in item.text or 'Successful' in item.text or 'En route' in item.text):
                        #print(item.text)
                        #print('---------------------------------')
                        success += 1


                    if exist == 0 and success != 0:
                        exist = 1

                        if launch_date in launch_dic:
                            launch_dic[launch_date] += 1
                        else:
                            launch_dic[launch_date] = 1

                    #print(time_draft)
                    #print(dd)
                    #print(mm)

            #skip the title
            row += 1

        print(launch_dic)

        with open('output.csv', 'w+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["date","value"])

            #iterate all days of 2019
            start_date = datetime.datetime(2019, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
            end_date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
            for single_date in self.daterange(start_date, end_date):
                 if single_date in launch_dic:
                     writer.writerow([single_date.isoformat(), launch_dic[single_date]])
                 else:
                     writer.writerow([single_date.isoformat(), 0])



    def run(self):
        self.get_res(self.start_url)



if __name__ =='__main__':
    orbi = orbital()
    orbi.run()