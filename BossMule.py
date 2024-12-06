import heapq

import pandas as pd
from sheets import access_google_sheet

crystal_prices_url = "https://docs.google.com/spreadsheets/d/1J6SF6v7Kn6b6bcqO5umas_1wN6UHApoQt5_L8cxjhdE/edit?usp=sharing"
crystal_prices_df = access_google_sheet(crystal_prices_url)

class BossingMule:
    _max_crystals = 14

    _bosses_run = [] #make this a min heap based on boss crystal values so that lower crystal prices get removed

    _income = 0
    _num_crystals = 0

    def __init__(self, name: str):
        self._name = name
        

    def add_crystal(self, boss: str, mode: str, party_size: int = 1) -> None:
        boss = boss.title()
        mode = mode.title()
        
        #Checks
        valid_mode = crystal_prices_df['Difficulty'].unique()
        if mode not in valid_mode:
            raise ValueError(f"Mode {mode} must be one of {valid_mode}")
        valid_boss = crystal_prices_df['Name'].unique()
        if boss not in valid_boss:
            raise ValueError(f"Boss {boss} mus  t be one of {valid_boss}")
        if boss in self.bosses_run():
            raise ValueError(f"Already running {boss}. Remove this boss first. Will implement automatic overwrite later.")
        
        crystal_value = crystal_prices_df.loc[(crystal_prices_df['Name'] == boss) & (crystal_prices_df['Difficulty'] == mode), "Price"].values[0]
        crystal_value //= party_size

        if len(self._bosses_run) < self._max_crystals: #Then you can run another boss on that mule
            heapq.heappush(self._bosses_run, (crystal_value, mode, boss))
            self._income += crystal_value
            self._num_crystals += 1
        else: #we need to remove a crystal as well to keep the count at a maximum of 14. We'll remove the lowest crystal using the min heap
            lowest_crystal = heapq.heappushpop(self._bosses_run, (crystal_value, mode, boss))
            self._income -= lowest_crystal[0]
            self._income += crystal_value
            
            print(f"Currently {self._name} sells 14 crystals. Adding {mode} {boss} and removing {lowest_crystal[1]} {lowest_crystal[2]}.")
            print(f"Change in boss mule income: {crystal_value - lowest_crystal[0]}")

        return
    
    def remove_crystal(self, boss: str) -> None:
        boss = boss.title()
        if boss in self.bosses_run():
            for i in range(self._num_crystals):
                crystal_val, mode, boss_name = self._bosses_run[i]
                if boss == boss_name:
                    print(f"Removing {mode} {boss}")
                    del self._bosses_run[i]
                    heapq.heapify(self._bosses_run)
                    self._num_crystals -= 1
                    break
        else:
            print(f"Crystal for {boss} not currently being sold. Please choose one of {self.bosses_run()}")
        return 
    
    #getters and setters
    def income(self):
        return self._income
    
    def crystal_count(self):
        return self._num_crystals
    
    def bosses_run(self):
        bosses_run = self._bosses_run.copy()
        return [heapq.heappop(bosses_run)[-1] for _ in range(len(bosses_run))]


if __name__ == "__main__":
    hero = BossingMule("SecondDeaI")
    hero.add_crystal("Kalos", "Normal", 1)
    hero.add_crystal("Kaling", "Normal", 6)
    hero.add_crystal("Verus Hilla", "Hard", 1)
    hero.add_crystal("Darknell", "Hard", 1)
    hero.add_crystal("Gloom", "Chaos", 1)
    hero.add_crystal("Seren", "Hard", 1)
    hero.add_crystal("Lotus", "Extreme", 2)
    hero.add_crystal("Will", "Hard", 1)
    hero.add_crystal("Lucid", "Hard", 1)
    hero.add_crystal("Damien", "Hard", 1)
    hero.add_crystal("Akechi", "Normal", 1)
    hero.add_crystal("Slime", "Chaos", 1)
    hero.add_crystal("Papulatus", "Chaos", 1)
    hero.add_crystal("Vellum", "Chaos", 1)
    hero.add_crystal("Magnus", "Hard", 1)
    hero.remove_crystal("Akechi")
    print(hero.bosses_run())
    print(hero.income())