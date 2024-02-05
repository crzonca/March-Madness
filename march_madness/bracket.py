import networkx as nx
from Projects.ncaam.march_madness import TeamsInfo


class Bracket:
    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def size(self):
        if self.is_leaf():
            return 1
        else:
            return self.left.size() + self.right.size()

    def to_graph(self):
        schools_mapping = TeamsInfo.map_schools_to_full_name()
        graph = nx.DiGraph()
        if self.is_leaf():
            graph.add_node(schools_mapping.get(self.label, self.label))
        else:
            left_graph = self.left.to_graph()
            right_graph = self.right.to_graph()

            graph.add_edge(schools_mapping.get(self.right.label, self.right.label),
                           schools_mapping.get(self.label, self.label))
            graph.add_edge(schools_mapping.get(self.left.label, self.left.label),
                           schools_mapping.get(self.label, self.label))

            graph = nx.compose(graph, left_graph)
            graph = nx.compose(graph, right_graph)
        return graph


def mm_bracket():
    play_in_1 = Bracket('Play In 1', Bracket('Southern'), Bracket('Green Bay'))
    play_in_2 = Bracket('Play In 2', Bracket('North Carolina Central'), Bracket('Central Connecticut'))
    play_in_3 = Bracket('Play In 3', Bracket('Seton Hall'), Bracket('Memphis'))
    play_in_4 = Bracket('Play In 4', Bracket('Colorado'), Bracket('Boise State'))

    r32_1_champ = Bracket('Round of 32 1', Bracket('Purdue'), play_in_1)
    r32_2_champ = Bracket('Round of 32 2', Bracket("Saint John's"), Bracket('New Mexico'))
    r32_3_champ = Bracket('Round of 32 3', Bracket('Baylor'), Bracket('Appalachian State'))
    r32_4_champ = Bracket('Round of 32 4', Bracket('Auburn'), Bracket('Akron'))
    r32_5_champ = Bracket('Round of 32 5', Bracket('Utah State'), Bracket('Grand Canyon'))
    r32_6_champ = Bracket('Round of 32 6', Bracket('Kansas'), Bracket('Drexel'))
    r32_7_champ = Bracket('Round of 32 7', Bracket('Clemson'), Bracket('Nebraska'))
    r32_8_champ = Bracket('Round of 32 8', Bracket('Marquette'), Bracket('Colgate'))

    r32_9_champ = Bracket('Round of 32 9', Bracket('North Carolina'), play_in_2)
    r32_10_champ = Bracket('Round of 32 10', Bracket('TCU'), Bracket('Mississippi State'))
    r32_11_champ = Bracket('Round of 32 11', Bracket('BYU'), Bracket('McNeese State'))
    r32_12_champ = Bracket('Round of 32 12', Bracket('Illinois'), Bracket('Samford'))
    r32_13_champ = Bracket('Round of 32 13', Bracket('South Carolina'), Bracket('Indiana State'))
    r32_14_champ = Bracket('Round of 32 14', Bracket('Creighton'), Bracket('Morehead State'))
    r32_15_champ = Bracket('Round of 32 15', Bracket('Texas Tech'), Bracket("Saint Mary's"))
    r32_16_champ = Bracket('Round of 32 16', Bracket('Arizona'), Bracket('Eastern Washington'))

    r32_17_champ = Bracket('Round of 32 17', Bracket('UConn'), Bracket('Eastern Kentucky'))
    r32_18_champ = Bracket('Round of 32 18', Bracket('Michigan State'), Bracket('Texas'))
    r32_19_champ = Bracket('Round of 32 19', Bracket('Kentucky'), Bracket('Richmond'))
    r32_20_champ = Bracket('Round of 32 20', Bracket('Iowa State'), Bracket('Cornell'))
    r32_21_champ = Bracket('Round of 32 21', Bracket('San Diego State'), play_in_3)
    r32_22_champ = Bracket('Round of 32 22', Bracket('Duke'), Bracket('Vermont'))
    r32_23_champ = Bracket('Round of 32 23', Bracket('Northwestern'), Bracket('Providence'))
    r32_24_champ = Bracket('Round of 32 24', Bracket('Tennessee'), Bracket('Quinnipiac'))

    r32_25_champ = Bracket('Round of 32 25', Bracket('Houston'), Bracket('South Dakota State'))
    r32_26_champ = Bracket('Round of 32 26', Bracket('Mississippi'), Bracket('Utah'))
    r32_27_champ = Bracket('Round of 32 27', Bracket('FAU'), Bracket('UC Irvine'))
    r32_28_champ = Bracket('Round of 32 28', Bracket('Dayton'), Bracket('Charlotte'))
    r32_29_champ = Bracket('Round of 32 29', Bracket('Oklahoma'), play_in_4)
    r32_30_champ = Bracket('Round of 32 30', Bracket('Alabama'), Bracket('High Point'))
    r32_31_champ = Bracket('Round of 32 31', Bracket('Colorado State'), Bracket('TAMU'))
    r32_32_champ = Bracket('Round of 32 32', Bracket('Wisconsin'), Bracket('Sam Houston State'))

    ss1_champ = Bracket('Sweet 16 1', r32_1_champ, r32_2_champ)
    ss2_champ = Bracket('Sweet 16 2', r32_3_champ, r32_4_champ)
    ss3_champ = Bracket('Sweet 16 3', r32_5_champ, r32_6_champ)
    ss4_champ = Bracket('Sweet 16 4', r32_7_champ, r32_8_champ)
    ss5_champ = Bracket('Sweet 16 5', r32_9_champ, r32_10_champ)
    ss6_champ = Bracket('Sweet 16 6', r32_11_champ, r32_12_champ)
    ss7_champ = Bracket('Sweet 16 7', r32_13_champ, r32_14_champ)
    ss8_champ = Bracket('Sweet 16 8', r32_15_champ, r32_16_champ)
    ss9_champ = Bracket('Sweet 16 9', r32_17_champ, r32_18_champ)
    ss10_champ = Bracket('Sweet 16 10', r32_19_champ, r32_20_champ)
    ss11_champ = Bracket('Sweet 16 11', r32_21_champ, r32_22_champ)
    ss12_champ = Bracket('Sweet 16 12', r32_23_champ, r32_24_champ)
    ss13_champ = Bracket('Sweet 16 13', r32_25_champ, r32_26_champ)
    ss14_champ = Bracket('Sweet 16 14', r32_27_champ, r32_28_champ)
    ss15_champ = Bracket('Sweet 16 15', r32_29_champ, r32_30_champ)
    ss16_champ = Bracket('Sweet 16 16', r32_31_champ, r32_32_champ)

    ee1_champ = Bracket('Elite 8 1', ss1_champ, ss2_champ)
    ee2_champ = Bracket('Elite 8 2', ss3_champ, ss4_champ)
    ee3_champ = Bracket('Elite 8 3', ss5_champ, ss6_champ)
    ee4_champ = Bracket('Elite 8 4', ss7_champ, ss8_champ)
    ee5_champ = Bracket('Elite 8 5', ss9_champ, ss10_champ)
    ee6_champ = Bracket('Elite 8 6', ss11_champ, ss12_champ)
    ee7_champ = Bracket('Elite 8 7', ss13_champ, ss14_champ)
    ee8_champ = Bracket('Elite 8 8', ss15_champ, ss16_champ)

    ff1_champ = Bracket('Final 4 1', ee1_champ, ee2_champ)
    ff2_champ = Bracket('Final 4 2', ee3_champ, ee4_champ)
    ff3_champ = Bracket('Final 4 3', ee5_champ, ee6_champ)
    ff4_champ = Bracket('Final 4 4', ee7_champ, ee8_champ)

    left_champ = Bracket('Championship 1', ff1_champ, ff2_champ)
    right_champ = Bracket('Championship 2', ff3_champ, ff4_champ)

    champ = Bracket('Winner', left_champ, right_champ)

    return champ
