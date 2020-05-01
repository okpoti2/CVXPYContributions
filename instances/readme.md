  Mutual capacity file (*.mut): 

  < mutual capacity pointer > , < mutual capacity >

  Arc file (*.arc):

  < arc name > , < from node > , < to node > , < commodity > , < cost > ,
  < capacity > , < mutual capacity pointer >

  Arc name is an integer between 1 and the number of arcs (differently from
  the original mnetgen format), that is necessary to distinguish between
  multiple instances of an arc (i, j) for the same commodity, that are
  permitted

  Node supply file (*.nod if FOUR_F == 0, *.sup otherwise):

  < node > , < commodity > , < supply >

  Problem description file (*.nod, only if FOUR_F == 1)

  < commodities > , < nodes > , < arcs > , < capacitated arcs >
