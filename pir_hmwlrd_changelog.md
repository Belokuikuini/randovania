# Command

## Command Courtyard
 - Documented Door to Lift Hub -> Event - Grapple Voltage Barrier ; Hazards without Hazard Shield

## Flux Center
 - Documented Morph Ball Door to Command Courtyard -> Pickup (Missile Expansion) ; SSJ & Space Jump
 - Documented Lower Level -> Morph Ball Door to Command Courtyard ; Space Jump & SSJ/Slope Jump

# Research

## Scrapvault
 - Documented Room Center -> Pickup (Missile Expansion)

 - Modified Door to Processing Access -> Room Center ;
  - Any of the following:
   - After Scrapvault Wall
   - Knowledge (Intermediate) and Disabled Entrance Randomizer

 Reason : While this is a trick that requires room transitions, it is a way to make reverse Research into a complete 
 loop, though it would also need for the door to be able to be opened if playing DLR. Might be worth refining,
 but perfectly understandable for this change to not cut it for now

## Processing Access
 - Documented Door to Scrapvault -> Pickup (Ship Missile Expansion) Knowledge and Hypermode

## Metroid Processing
 - Added new Node : Room Center

 - Removed connection : Door to Processing Access -> Basement
 - Added connection : Door to Processing Access -> Room Center ; Grapple Lasso or Combat (Beginner) or Enter Hypermode
 - Added connection : Room Center -> Door to Processing Access ; Grapple Lasso or Combat (Beginner) or Enter Hypermode
 (The reason for these requirements is the lockdown can still be triggered if not coming from Processing Access)
 - Added connection : Room Center -> Basement ; X-Ray Visor

 - Removed connection : Door to Processing Access -> Top Floor
 - Added connection : Room Center -> Top Floor ;
  - All of the following :
   - Morph Ball
   - Any of the following :
    - After Metroid Processing Ball Lift
    - Boost Ball and Spider Ball
    - Space Jump Boots and Bomb/Spring Space Jump (Beginner)
 - Added connection : Top Floor -> Room Center : Trivial

 Reason : The Pirates in this Room's scripted fight carry shields, which makes them non-trivial to kill when
 the player has neither Lasso or Hypermode to break the shields. Plus, the fight trigger is by the door to 
 Processing Access, which makes it possible to skip the fight entierly if coming from Airshaft or Creche Transit 
 and going to either of these rooms without going to the Basement
