- Player
    - Actions
        - Turn
        - Accelerate
        - Pass
        - Shoot
        - Steal

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
        - Belongs to player
        - Mid pass
        - Mid shot
        - Loose ball
    

- Game
    - Players
    - Ball
    - Court
        
        
