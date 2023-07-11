from boss_crystal import Crystal

class Bosser:
    boss_crystals = []
    clear_time = 0
    buff_freezers_used = 0
    ran = False

    def __init__(self, name: str, job: str, level: str) -> None:
        self.name = name
        self.job = job
        self.level = level

    def add_crystal(self, boss_name: str, boss_type: str, party_size: int, clear_time: int) -> None:
        crystal = Crystal(boss_name, boss_type, party_size, clear_time)
        self.boss_crystals.append(crystal)


    def remove_crystal(self, boss_name: str, boss_type: str, party_size: int, clear_time: int) -> None:
        crystal = Crystal(boss_name, boss_type, party_size, clear_time)
        self.boss_crystals.remove(crystal)


    def set_freezers(self, num: int) -> None:
        self.buff_freezers_used = num


    def toggle_run_status(self) -> None:
        if not ran:
            ran = True
        else:
            ran = False


    def total_mesos(self) -> int:
        total = 0
        for crystal in self.boss_crystals:
            total += crystal.crystal_value
        total -= self.buff_freezers_used * 5_000_000
        return total
    

    def total_time(self) -> int:
        total = 0
        for crystal in self.boss_crystals:
            total += crystal.clear_time
        return total
    

    def clear_crystals(self) -> None:
        boss_crystals = []
        clear_time = 0 


if __name__=='__main__':
    seconddeal = Bosser("SecondDeaI", "Hero", "271")
    seconddeal.add_crystal("BlackMage", 'Hard', 6, 25)
    seconddeal.add_crystal("Magnus", 'Hard', 1, 4)
    print(seconddeal.boss_crystals)
    print(seconddeal.total_mesos(), seconddeal.total_time())