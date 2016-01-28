"""Shogi Kifu Analyzer

usage: shogi_kifu_analyzer.py [-h | --help]

options:
    -h, --help  show this help message and exit
"""

from docopt import docopt
from collections import defaultdict
import shogi.KIF
import sys

#shogi.Board.sfen()が返す情報から何手目かの情報を落としてキーとして利用する辞書
#このクラスからSEFNの情報を復元する際、全て「0手目の局面」(次が1手目)として返す
class ShogiDict():
    def __init__(self):
        self.__dict__ = defaultdict(int)

    #SFENの情報から「何手目か」を落とす
    def cut_number_information_from_sfen(self, sfen_str):
        return " ".join(sfen_str.split(' ')[0:-1])

#SFEN文字列(ただし、次何手目かの情報は落とす)がキー、その局面が現れた回数が値
class KyokumenDict(ShogiDict):
    def add(self, sfen_str):
        self.__dict__[self.cut_number_information_from_sfen(sfen_str)] += 1

    def items(self):
        return [(k + " 1", v) for k,v in self.__dict__.items()]

#SFEN文字列とその局面からの移動(USI表現)のタプルがキー、その回数が値
class EdgeDict(ShogiDict):
    def add(self, sfen_str, move):
        key = (self.cut_number_information_from_sfen(sfen_str), move)
        self.__dict__[key] += 1

    def items(self):
        return [((k[0]+" 1", k[1]), v) for k,v in self.__dict__.items()]

class ShogiKifuAnalyzer:
    def __init__(self):
        self.kif_list = []
        self.kyokumen_dict = KyokumenDict()
        self.edge_dict = EdgeDict()

    def load_kif(self, kif_file_name):
        kif = shogi.KIF.Parser.parse_file('converted_kif/' + kif_file_name)[0]
        board = shogi.Board()

        self.kyokumen_dict.add(board.sfen())

        for move in kif["moves"]:
            self.edge_dict.add(board.sfen(), move)
            board.push_usi(move)
            self.kyokumen_dict.add(board.sfen())

        self.kif_list.append(kif)

    # def get_kifs(self):
    #     return self.kif_list

    def get_kyokumen_dict(self):
        return self.kyokumen_dict


def main():
    args = docopt(__doc__)

    analyzer = ShogiKifuAnalyzer()
    for kif_file_name in sys.stdin:
        kif_file_name = kif_file_name.rstrip()
        analyzer.load_kif(kif_file_name)

    kyokumen_dict = analyzer.get_kyokumen_dict()

    for sfen, freq in sorted(kyokumen_dict.items(), key=lambda x:x[1])[::-1]:
        print(shogi.Board(sfen).kif_str())
        # print("%d %s" % (freq, sfen))

    return

if __name__ == '__main__':
    main()
