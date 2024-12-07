from typing import List
from BossMule import BossingMule
from sheets import access_google_sheet
from pandas import DataFrame
import heapq

class Account:

    _maximum_crystals = 180
    _maximum_crystals_per_character = 14

    def batch_insert_bosses(self, bossmule: BossingMule, group: DataFrame, verbose = False) -> BossingMule:
        for index, charname, difficulty, boss_name, party_size in group.itertuples():
            try:
                crystal_price = bossmule.add_crystal(boss_name, difficulty, party_size)
                heapq.heappush(self._alL_bosses, (crystal_price, boss_name, charname))
                if verbose:
                    print(f"Adding {difficulty} {boss_name}")
            except ValueError as e:
                if verbose:
                    print(e)
        return bossmule


    def remove_excess_bosses(self, verbose: bool = False):
        f"""Pops n smallest crystals from all bosses until Account only has {self._maximum_crystals} to sell. Each bossing mule is automatically constrained to their highest {self._maximum_crystals_per_character} crystals"""
        while self._crystals_sold > self._maximum_crystals:
            crystal_price, boss_name, character = heapq.heappop(self._alL_bosses)
            if verbose:
                print(f"Currently selling {self._crystals_sold - self._maximum_crystals}, removing {crystal_price} meso crystal from {boss_name} from {character}.")
            self._crystals_sold -= 1
            self._income -= crystal_price
            #Remove the crystal from the given boss mule
            BM = self._bossers[character]
            BM.remove_crystal(boss_name)
            if BM.crystal_count() == 0:
                #You've removed the only crystal from this character.
                del self._bossers[character]
                self._num_bossers -= 1
                if verbose:
                    print(f"{character} no longer selling crystals. Removing {character} from roster. You have {self._num_bossers} remaining.")

        return


    def __init__(self, spreadsheet: str) -> None:

        self._income = 0
        self._crystals_sold = 0 #must stay at or below 180
        self._num_bossers = 0 
        self._bossers = {}
        self._alL_bosses = []
        self._run_status = {}

        df = access_google_sheet(spreadsheet)
        self._bosser_df = df.copy()

        bosser_names = df['Character'].unique()
        for name, group in df.groupby(df.columns[0]):
            try:
                BM = BossingMule(name)
                self.batch_insert_bosses(BM, group)
                self._crystals_sold += BM.crystal_count()
                self._income += BM.income()
                self._bossers[name] = BM
                self._num_bossers += 1  
                self._run_status[name] = False
            except Exception as e:
                print(e)

        self.remove_excess_bosses(True)

        return

    
    def __repr__(self):
        return f"Account with {self._num_bossers} bossing characters. {self._income} mesos with {self._crystals_sold} sold"

    def update_status(self, character_name, status):
        self._run_status[character_name] = status
        return

    def bossers(self):
        return self._bossers.values()
    
    def income(self):
        return self._income
    
    def crystal_count(self):
        return self._crystals_sold

    def view_bosses(self):
        return dict(zip(self._bossers.keys(), [x.bosses_run() for x in self.bossers()]))


    
if __name__=='__main__':
    my_account_spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-LOEXqRyDN923dNaG6kmogCqdKQzUSl34wqwNJvPqqY/edit?usp=sharing"
    my_account = Account(my_account_spreadsheet_url)
    print(my_account)
    print(my_account.view_bosses())

    for bosser in my_account.view_bosses():
        print(bosser, my_account.view_bosses()[bosser])