Contents:
  Agents:
    spinAgent.py
    spinAimAgent.py
    spinAimDodgeAgent.py
  Agent Resources:
    common.py
  Development Resources:
    asteroid-pixel-count.py
    common-test.py 
    datatools
    ship-pixel-count.py

Instructions:
  To run any of the agents, use the following command:
    python [agent file name]

  To run the unit test suite, use the following command:
    python common-test.py

  To run the asteroids environment with a motionless agent and count all 
  the asteroid pixels using the common library's isAsteroid function,
  use the following command:
    python asteroid-pixel-count
    
  Note that this does not need to run to completion to gather data. data
  collected will be written to a file of the following naming format
    asteroid_count_YYMMDD_HHMMSS.txt
  
  The date and time correspond with the date and time 
  asteroid-pixel-count.py was run to gather the data in the file.
  
  To do the same as previously described for ship pixels, use the
  following command:
    python ship-pixel-count
    
  This will produce text files of the following naming format:
    ship_count_YYMMDD_HHMMSS.txt
    