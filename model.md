- Player
    - Actions
        - Turn
        - Accelerate
        - With ball
            - Pass
            - Shoot

    - State
        - Physics
            - Position
            - Velocity
            - Orientation
        - Ball Handling
            - Has ball
            - Time since catch
 
    - Attributes
        - Physical
            - max accel
            - max turn
            - velocity damping
        - Offensive Ability
            - Shot Probability (Distance, Player.State)
            - Dribbling Speed Penalty
        - Defensive Ability
            - Shot % Reduction (Distance)

- Shot Probability
    - Attacker Player.Skill
    - Defenders List[Player.Skill]
    - Court Position
        - Angle to Hoop
        - Distance to Hoop


- Ball
    - Physics
        - Position
        - Velocity
        - Orientation
    - States
        - Held
        - Mid pass
        - Mid shot
        - Dead ball

- Game
    - State
        - Teams
            - Players
        - Ball
        - Court
            - Boundary
            - Three point region
            - Hoop locations
        - Possession
            - Team
            - Clock
        - Stats
            - Team score
            - Player stats
    - Actions
        - Check Players
            - determine if shooting foul => Dead (free throws, baseline out)
            - determine if off ball foul => Dead (side or baseline out)
            - determine if offensive foul => Dead (turnover, baseline out)
        - Check Ball
            - If held
                - determine if out of bounds => Dead (side or baseline out)
                - determine if stolen/poked => Held (turnover) or Loose
                - determine if lost handle => Loose
            - If mid pass
                - determine if out of bounds => Dead (side or baseline out)
                - determine if intercepted => Held (turnover) or Loose
            - If post pass
                - determine if receiver catches successfully => Held
                - determine if receiver fumbles catch => Loose
            - If mid shot
                - determine if intercepted/blocked => Held (live ball turnover) or Loose
            - If post shot
                - determine if shot missed => Loose
                - determine if made shot => Held (reset)




    
        
