from typing import List
from BossMule import BossingMule
from sheets import access_google_sheet

class Account:

    _income = 0
    _crystals_sold = 0 #must stay at or below 180
    _num_bossers = 0 
    _bossers = []

    def add_bosser(self, boss_mule: BossingMule) -> None:
        
        self._crystals_sold += boss_mule.crystal_count()
        self._income += boss_mule.income()
        self._num_bossers += 1

        return

    def __init__(self, spreadsheet: str) -> None:
    
        df = access_google_sheet(spreadsheet)
        self._bosser_df = df.copy()

        for bosser_name, group in df.groupby(df.columns[0]):
            BM = BossingMule(bosser_name)
            for index, _, difficulty, boss_name, party_size in group.itertuples():
                try:
                    BM.add_crystal(boss_name, difficulty, party_size)
                except ValueError as e:
                    print(e)
            self._bossers.append(BM)

        return
    
    def bossers(self):
        return self._bossers
    
    def income(self):
        return self._income
    
    def crystal_count(self):
        return self._crystals_sold

    
if __name__=='__main__':
    my_account_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-LOEXqRyDN923dNaG6kmogCqdKQzUSl34wqwNJvPqqY/edit?usp=sharing"
    my_account = Account(my_account_spreadsheet_url)