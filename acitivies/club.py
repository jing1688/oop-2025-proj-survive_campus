# from entities.player import Player

class Club:
    def __init__(self, player):
        """
        初始化社團系統，綁定一個 Player 物件。
        
        參數:
            player (Player): 玩家實例，用來修改其屬性
        """
        self.player = player

    def join_club(self):
        """
        參加社團:
            - 能量 -20
            - 時間 +5
            - 金錢 -700
            - 社交 +2
            - 探索 +2
        
        回傳:
            (bool, str): 第一個值為是否成功（是否有足夠資源），
                         第二個值為提示訊息。
        """
        if self.player.energy < 20:
            return False, "能量不足，無法參加社團。"
        if self.player.money < 700:
            return False, "金錢不足，無法參加社團。"

        self.player.energy    -= 20
        self.player.money     -= 700
        self.player.social    += 2
        self.player.explore   += 2

        return True , "你參加了社團。"

    def peer_gathering(self):
        """
        同儕聚會:
            - 能量 -20
            - 時間 +4
            - 金錢 -800
            - 社交 +3
            - 健康 +1
        
        回傳:
            (bool, str): 第一個值為是否成功（是否有足夠資源），
                         第二個值為提示訊息。
        """
        if self.player.energy < 20:
            return False, "能量不足，無法參加同儕聚會。"
        if self.player.money < 800:
            return False, "金錢不足，無法參加同儕聚會。"

        self.player.energy    -= 20
        self.player.money     -= 800
        self.player.social    += 3
        self.player.health    += 1
        return True, "你參加了同儕聚會。"