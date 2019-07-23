from cg.clobber import Clobber


c = Clobber("LLR") + Clobber("LRR")
print(c.board_str())
print(c.canonical_form())
print((-c).board_str())
