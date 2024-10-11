from time import sleep
import os
import random
from random import randint
import threading
import time
import sys

msg=""
inventory={}
maxzombi = 10  #Max value for health bar
minzombi= 0
playerzombi = 1 # players current health
survivor_count = 0 # tracks number of survivors with player
max_hunger=10 #max hunger before player dies
player_hunger= 10 #tracks players current hunger level
game_over = False #this is what we will use for all deaths and use for function to restart game
hpdisplay = chr(0x2588) + chr(0x2502)
dashdisplay = chr(0x2591) + chr(0x2502)
hunger_message = ""
ascii_art = {
    "landing_room": """                                   _______________________      |
                                  |  ________   ________  |     |
                                  | |        | |    ___ | |     |
                                  | |        | |  ,',.('| |     |
                                  | |        | | :  .'  | |     |
                                  | |        | | :) _  (| |     |
                                  | |        | |  `:_)_,| |     |
                                  | |________| |________| |     |
                                  |  ________   ________  |     |
                                  | |        | |        | |     |
                                  | |        | |        | |     |
                                  | |        | |        | |     |
                                  | |        | |        | |     |
                                  | |        | |        | |     |
                                  | |________| |________| |     |
                                  |_______________________|     |
                                                                |
                                                                |
                   _____________________________________________|
                                                                `.
                                                                  `.
                                                                    `.
                                                                      `.
                     ..::::::::::::' .:::::::::::::::                   `.
                 ..:::::::::::::::' .:::::::::::::::'                     `
             ..:::::::::::::::::' .:::::::::::::::::
         ..::::::::::::::::::::' .:::::::::::::::::'
     ..::::::::::::::::::::::' .:::::::::::::::::::
 ..:::::::::::::::::::::::::' .:::::::::::::::::::'
..........................  ......................
:::::::::::::::::::::::::' .:::::::::::::::::::::'
:::::::::::::::::::::::' .:::::::::::::::::::::::
::::::::::::::::::::::' .:::::::::::::::::::::::'
::::::::::::::::::::' .:::::::::::::::::::::::::
:::::::::::::::::::' .:::::::::::::::::::::::::'          """,

"forest":  """
                          (    )
                           (    )
                          (    )
                            )  )
                           (  (                  /\.
                            (_)                 /  \  /\.
                    ________[_]________      /\/    \/  \.
           /\      /\        ______    \    /   /\/\  /\/\.
          /  \    //_\       \    /\    \  /\/\/    \/    \.
   /\    / /\/\  //___\       \__/  \    \/
  /  \  /\/    \//_____\       \ |[]|     \.
 /\/\/\/       //_______\       \|__|      \.
/      \      /XXXXXXXXXX\                  \.
        \    /_I_II  I__I_\__________________\.
               I_I|  I__I_____[]_|_[]_____I
               I_II  I__I_____[]_|_[]_____I
               I II__I  I     XXXXXXX     I
            ~~~~~"   "~~~~~~~~~~~~~~~~~~~~~~~~                     """,

"town": """

                   \  |  /         ___________
    ____________  \ \_# /         |  ___      |       _________
   |            |  \  #/          | |   |     |      | = = = = |
   | |   |   |  |   \/#           | |`v'|     |      |         |
   |            |    \#  //       |  --- ___  |      | |  || | |
   | |   |   |  |     #_//        |     |   | |      |         |
   |            |  \/ #_/_______  |     |   | |      | |  || | |
   | |   |   |  |   \/# /_____/ \ |      ---  |      |         |
   |            |    \# |+ ++|  | |  |^^^^^^| |      | |  || | |
   |            |    \# |+ ++|  | |  |^^^^^^| |      | |  || | |
^^^|    (^^^^^) |^^^^^#^| H  |_ |^|  | |||| | |^^^^^^|         |
   |    ( ||| ) |     # ^^^^^^    |  | |||| | |      | ||||||| |
   ^^^^^^^^^^^^^________/  /_____ |  | |||| | |      | ||||||| |
        `v'-                      ^^^^^^^^^^^^^      | ||||||| |   """,
"local spoons": """

                                   .-.,-.
                                  _|_||_|_
                                ,'|--'  __|
                                |,'.---'-.'
  ___                            |:|] .--|
 (__ ```----........_________...-|-|__'--|-........_________.....
  \._,```----........__________..::|--' _|--........_________....
  :._,._,._,._,._,._,._,._,._,._,\/|___'-|._,._,._,._,._,._,._,._
  |._,._,._,._,._,._,._,._,._,._,.`'-----'._,._,._,._,._,._,._,._
  |._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._
  |._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._
  ;._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._
 /,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._,._
 )________)________)________)________)________)________)_______)_
  |::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::.-
  |_|_  .----._     ___.-_-__-_-.--.-'          __.-.-_-__-_-. '-
  |---' '--.-'-'.  '-.-||_|__|_||--'           '--'-||_|__|_||_
  |        '----'    '-|| |  | ||             ____.-|| |  | ||-'
  |                   [||-|--|-||_           '--.-'-||-|--|-||
  |-.____              ||_|__|_||-'-.           '---||_|__|_||_ _
  |-'-.--'       ___.--||_|__|_||---' ___.--.       ||_|__|_||_'-
  |---'         '---'--'--------'    '---'--'       '--------'
  ;--.______________________________________________,--._________
  :(o))---------------------------------------------:(o))--------
  |`-: \//|[_  /,.\|| |,\|[_  ((_ |[]|/,.\|o)|o)|[_ |`-: ((_ |||
  |__| // |[_  \`'/|'-|`/|[_   _))|[]|\`'/|| || |[_ |__|  _))|||`
  |--|____________________________________________  |--|  _______
  |  |       |`-||__|--|__|--|__|--|__|--|__|--|__| |__| ||__|--|
  |  |_____  |._|.-------..-------..-------..----.| |  | |.------
  |  |.-.-.| |  ||::'    ||::'    ||::'    ||:'  || |  | ||:'
  |  || | || |  ||'      ||'      ||'      ||    || |  | ||____.:
  |  ||-|-|| |  ||       ||       ||       ||    || |  | |.------
  |  || | || |  ||      .||      .||      .||    || |  | ||:'
  |__|'-'-'|/:._||___..::||___..::||___..::||__.:|| |__| ||____.:
  |  |     || `-|---------------------------------.'|  |'.-------
 _|__|-----''-..| ________________________________|_|__|_|_______   """,

}
locations = {
    "landing_room": {
        "description": "You are in the landing room. You quickly glance around the room, taking in the surrounding area.\n It appears to be a regular living room, but the furniture is smashed to pieces and thrown across the room as if someone was searching for something or in a violent rage.\n Only a few things are still standing in the room.",
        "options": {
            "1": {"description": "Look around the room", "next": "searched_room"},
            "2": {"description": "Leave the house", "next": "outside"}
        },
        "visited": False
    },
    "searched_room": {
        "description": "You rummage around the room and find a Medkit tucked away under a pile of rubble.",
        # "item": "Medkit",
        "options": {
            "2": {"description": "Leave the house", "next": "outside"}
        },
        "visited": False
    },
    "outside": {
        "description": "You are outside the house.\n You see a long winding path with flowers covering most of it, leading towards a mysterious-looking forest with tall, dark trees making it hard to see into.\n Alongside it, you see another path, a more modern brick path with a clearly broken street light flickering randomly, illuminating a sign pointing towards the nearest town.",
        # "item": "Ration",
        "options": {
            "1": {"description": "Go to the forest", "next": "forest"},
            "2": {"description": "Go to the town", "next": "town"}
        },
        "visited": False
    },
    "forest": {
        "description": "The forest is dense and eerie. The trees block out most of the sun, allowing only a small amount of light to peer in.\n You feel like someone is watching you as you slowly walk through.\n It's as though you are seeing faces in the trees, or were they just past the trees?\n You see an abandoned cabin not far away.",
        "options": {
            "1": {"description": "Approach the cabin", "next": "cabin"},
            "2": {"description": "Return to outside the house", "next": "outside"}
        },
        "visited": False
    },
    "cabin": {
        "description": "As you approach the cabin, you notice a standing mail post by the fence of the property with a massive heart on its side.\n Inside the heart are the initials D+I, probably belonging to the previous owners.\n On the porch, there are two bowls—one dog-sized and one cat-sized—with the names Shy and Loki written on them, respectively.\n As you enter the cabin, you take in the interior.\n Against a wall, there is a massive sword next to a bow above a fireplace, with a photo of one of the owners on a majestic horse.\n Across from the fireplace sits a cute coffee table with books stacked on top of each other; at the top, you see 'The Song of Achilles.'\n You can tell the owners loved this place dearly.",
        # "item": ["Fasting_potion","Key"],
        "options": {
            "1": {"description": "Leave", "next": "forest"},
        },
        "visited": False
    },
    "town": {
        "description": "The town is deserted, with basically no noise except for the sound of rats scurrying around, searching for trash to eat.\n Down a street on your left you can see an abandoned store with its windows smashed in.\n There are still some supplies left that could help you on your journey.\n However you can hear the sound of human activity in the distance..... ",
        "options": {
            "1": {"description": "Enter the store", "next": "store"},
            "2": {"description": "You see people bustling in the distance", "next": "local_spoons"}
        },
        "visited": False
    },
    "local_spoons": {
        "description": "As you continue walking through the remains of the town, every place looks closed down and abandoned, with broken windows and abandoned cars in the streets.\n As you wander around, you start to lose hope of finding others until you hear a noise.\n It sounds like screams, but not of fear; it sounds like joy.\n You start running towards it, and as you turn the corner, you see a bar open with people inside.\n The windows have tables pushed up against them to prevent break-ins, and the only entrance you can see is a massive door with people stationed in front of it, likely keeping watch for zombies.",
        # "item": ["Bandages", "Key"],
        "options": {
            "1": {"description": "You decide its time to head to your old home", "next": "players_home"},
            "2": {"description": "You hear people talking about survivors being holed up in the old school", "next": "characters_sons_school"}
        },
        "visited": False
    },
    "players_home": {
        "description": "As you walk up to your home, memories of the place come flooding back.\n You remember when you first bought it with your partner,\n walking into the house after your wedding with your wife in your arms, and bringing your child home for the first time.\n It looks exactly as you remember it, except for the damages from the zombie attacks.\n You look around the interior of the room, and your eyes lock onto the door leading to what you remember being a basement.\n But if it was just a basement, why does the door look so metallic, as if it's trying to keep people out?",
        
        "options": {
            "1": {"description": "Return to the local spoons", "next": "local_spoons"},
            "2": {"description": "You see a note reading'going to museum'", "next": "museum"},
            "3": {"description": "Go to the basement", "next": "players_home_basement"},
            "4": {"description": "Go to a survivor community with your wife", "next": "survivor_community_with_wife" },
            "5": {"description": "Go to a survivor community with your son", "next": "survivor_community_with_son"},
            "6": {"description": "Go to a survivor community with your whole family", "next": "survivor_community_with_family"}
        },
        "visited": False
    },
    "players_home_basement": {
        "description": "As you slowly open the heavy door, you see nothing but a metallic staircase with a few dimly lit bulbs eerily inviting you down.\n As you make your way down, panic sets in—what if this is where it all started? What if there's nothing left?\n As you open the final door, you see walls lined with shelves and drawers filled with food, bandages, and supplies. This isn't where it started; it's a panic room for you and your family.",
        "visited": False
    },
    "characters_sons_school": {
        "description": "You arrive at what you remember being your son's school.\n It looks different now; most of the doors are boarded up except for one set of double doors.\n Upon closer inspection, you realise it's become a temporary safe place.\n However, you see zombies trying to break in from the sides, too many for the people to handle.\n You manage to rush in and find your son in time to get you both out before the attack.",
        # "item": "Son",
        "options": {
            "1": {"description": "Return home with your son", "next": "players_home"}
        },
        "visited": False
    },
    "museum": {
        "description": "You approach the massive building, older than any other in the area.\n The building looks untouched amidst all this madness.\n As you reach the door, you notice people inside hiding.",
        # "item":   "Wife",
        "options": {
            "1": {"description": "Return home with your wife", "next": "players_home"}
        },
        "visited": False
    },
    "survivor_community_with_wife": {
        "description": "As you and your wife approach the shelter, days of exhausting travel weigh heavily on your shoulders.\n The path is long, winding through barren fields and deserted towns.\n Each step is filled with the unspoken grief for your son, a pain that echoes in every shadow and quiet moment.\n When you finally reach the community, its high walls and guarded entrance promise safety, but the sense of relief is fleeting.\n The shelter may offer physical security, but nothing can protect against the ache of your loss, which lingers, heavy and unyielding, even within the confines of this new sanctuary.",
        "options": {
            "1": {f"description": "END GAME", "next": "{break}"}
        },
        "visited": False
    },
    "survivor_community_with_son": {
        "description": "After days of grueling travel, you and your son finally arrive at the safe community.\n Exhaustion hangs heavy in the air as the secure walls loom before you, offering a promise of safety that feels empty without her.\n Each step forward is weighed down by the absence of your wife,\n the grief a constant companion as you try to remain strong for your son.\n The community is quiet, the kind of silence that only serves as a reminder of what you've lost.\n You hold your son close, knowing that while you may be safe, the ache remains.",
        "options": {
        "1": {f"description": "END GAME", "next": "{break}"}
        },
        "visited": False
    },
    "survivor_community_with_family": {
        "description": "After days of grueling travel, you, your wife, and your son finally reach the shelter.\n The journey has been exhausting, taking you through rough terrain, abandoned towns, and sleepless nights.\n The weight of the struggle is heavy on all of you, but the sight of the high walls and the promise of safety offers a glimmer of hope.\n As you enter, you feel the tension ease, knowing that at least for now, you are together and protected.\n Despite the relief, there's a lingering fear—what you endured has left scars,\n and you know survival comes with its own battles.\n But, with your family by your side, there's still strength to keep moving forward.",
        "options": {
            "1": {f"description": "END GAME", "next": "{break}"}
        },
        "visited": False
    },
}
def add_to_inventory(item):
    if item in inventory:
        inventory[item] += 1
    else:
        inventory[item] = 1

def remove_from_inventory(item):
    if item in inventory and inventory[item] > 0:
        inventory[item] -= 1
        if inventory[item] == 0:
            del inventory[item]  # Remove the item if the quantity is 0
        print(f"You used {item}.")
        return True
    else:
        raise ValueError(f"You have no {item}.")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # call this function to clear the players screen before progressing

def show_controls_menu():
    clear()
    print("############## CONTROLS MENU ##############")
    print("Use Number buttons to navigate between scenarios")
    print("Press 'B' to use Bandages - Heal 1HP")
    print("Press 'M' to use Medkit - Heal 2HP")
    print("Press 'R' to eat Ration - Fill 1 hunger")
    print("Press 'F' to drink Fasting Potion - Fill 2 hunger and pay respect")
    print("\nPress 'Q' to go back to the game...")
    input("Press Enter to go back to the game...")  # Pauses until the player presses Enter
    clear()

def game_loop():
    while True:
        clear()
        print("Game running...")
        print("Press 'H' anytime to show the controls menu")
        print("\n[1] Continue playing")
      

# def rush():
#     global inventory
#     global playerzombi
#     chances=["fail","fail","fail","fail","fail","fail","fail","success","success","success"]
#     randnum=randint(0,len(chances))        
#     if randnum <= 7:
#         playerzombi +=2
#         print("You tried to rush through the store and grab everything you could.\n You tripped and fell and were attacked by 2 zombies,they got you good")
#     elif randnum> 7:
#         add_to_inventory("Medkit")
#         add_to_inventory("Fasting_potion")
# def stealth():
#     global inventory
#     global playerzombi
#     chances2=["fail","fail","success","success","success","success","success","success","success","success"]
#     randnum2= randint(0,len(chances2))
#     if randnum2<=2:
#         playerzombi +=1
#         print("you were sneaking about when a zombie casts detect, pinpointing your location\n You escape with just a scratch ")
#     elif randnum2>2:
#         add_to_inventory("Bandages")
#         add_to_inventory("Ration")

def zombification():
    global playerzombi
    # Ensure health is always clamped within the range but allow it to exceed for display purposes
    display_zombi = min(playerzombi, maxzombi)
    totalzombi = maxzombi - display_zombi
    dishp = hpdisplay * display_zombi
    dashzero = dashdisplay * totalzombi
    overall_health = dishp + dashzero
    return overall_health  # Always return the overall health string for display

def hunger():
    global player_hunger
    # Ensure hunger is clamped within the range but allow it to exceed for display purposes
    display_hunger = min(player_hunger, max_hunger)
    total_hunger = max_hunger - display_hunger
    dishp = hpdisplay * display_hunger
    dashzero = dashdisplay * total_hunger
    overall_hunger = dishp + dashzero
    return overall_hunger  # Always return the overall hunger string for display

def hunger_timer():
    global player_hunger, game_over
    while not game_over:
        time.sleep(60)  # Set to 60 seconds for the real game
        if player_hunger > 0:
            player_hunger -= 1
            player_hunger = max(0, player_hunger)  # Clamp to ensure it doesn't go negative
            print(f"\rYou have been on the move for a while. Hunger increased! Current hunger: {player_hunger}", end="")
            sys.stdout.flush()
            time.sleep(2)
            # Overwrite the line by moving the cursor back and clearing it
            print("\r" + " " * 80 + "\r", end="")
        if player_hunger == 0:
            print("\nYou starved to death: GAME OVER")
            game_over = True  # Set the game_over flag to end the game
            display_game_over_screen()
            break

def display_game_over_screen():
    clear()
    print("############################")
    print("#         GAME OVER        #")
    print("############################")
    print("\nRestarting the game in 5 seconds...")
    sleep(5)
    restart_game()

def restart_game():
    global player_hunger, playerzombi, game_over, survivor_count, inventory
    player_hunger = max_hunger  # Set to max_hunger
    playerzombi = maxzombi  # Set to maxzombi
    survivor_count = 0
    inventory = {}
    game_over = False
    clear()
    start_game()

def show_description(description):
    lines = description.split("\n")
    for line in lines:
        print(line)
        time.sleep(0.5)
        clear() 

def print_status(current_location):
    
    print("ZOMBIFICATION:", zombification())
    print("")
    print("HUNGER:       ", hunger())
    print("INVENTORY:")
    for item, quantity in inventory.items():
        print(f" - {item}: {quantity}")
    print(f"Survivor count = {survivor_count}\n{'-' * 27}")
    print("LOCATION:      ", current_location.replace("_", " ").title())
    print(msg)

def start_game():
    hunger_thread = threading.Thread(target=hunger_timer, daemon=True)
    hunger_thread.start()
    navigate_location("landing_room", 0)

def navigate_location(current_location, turns_taken):
    global msg, playerzombi, player_hunger, inventory
    
    location = locations[current_location]

    # Clear the screen first before showing the description or status
    clear()
    
    # Show the description only if the location hasn't been visited
    if not location.get("visited", False):
        show_description(location["description"])
        location["visited"] = True  # Mark as visited

    if not zombification() or game_over:
        return  # Exit the function if the player is dead
    if not hunger() or game_over:
        return
    
    # Print the ASCII art if it exists for the current location
    if current_location in ascii_art:
        print(ascii_art[current_location])  

    # Check for items in the location and add to inventory
    if "item" in location:
        item = location["item"]
        if item not in inventory:
            add_to_inventory(item)
            # Display the message about finding the item and add a delay
            print(f"You found a {item} and added it to your inventory.")
            sleep(2.0)
            clear()  # Clear the screen after the message and before showing the status
            del location["item"]  # Remove the item from the location to prevent multiple pickups

    # Call print_status to display the updated inventory
    print_status(current_location)

    # Display the available options
    for key, option in location["options"].items():
        # Check if the option has a requirement and if the player has the item
        if "requires" in option and option["requires"] not in inventory:
            print(f"[{key}] {option['description']} (You need a {option['requires']} to access this)")
        else:
            print(f"[{key}] {option['description']}")

    user_input = input("Choose an option: ")

    if user_input == 'H' or user_input == 'h':
        show_controls_menu()
        navigate_location(current_location, turns_taken)  # Return to the same location after showing menu

    # Process item usage
    if user_input == "B" or user_input == "b":
        try:
            remove_from_inventory("Bandages")
            playerzombi = max(minzombi, playerzombi - 1)  # Heal but keep within bounds
            print("You have used a bandage.")
            sleep(2.0)
        except ValueError as e:
            print(e)

    if user_input == "M" or user_input == "m":
        try:
            remove_from_inventory("Medkit")
            playerzombi = max(minzombi, playerzombi - 2)  # Heal but keep within bounds
            print("You have used a Medkit.")
            sleep(2.0)
        except ValueError as e:
            print(e)

    if user_input == "R" or user_input == "r":
        try:
            remove_from_inventory("Ration")
            player_hunger = min(max_hunger, player_hunger + 1)  # Increase but keep within max_hunger
            print("You have eaten a ration.")
            sleep(2.0)
        except ValueError as e:
            print(e)

    if user_input == "F" or user_input == "f":
        try:
            remove_from_inventory("Fasting_potion")
            player_hunger = min(max_hunger, player_hunger + 2)  # Increase but keep within max_hunger
            print("You pay your respects.")
            sleep(2.0)
        except ValueError as e:
            print(e)

    if user_input in location["options"]:
        option = location["options"][user_input]
        if "requires" in option and option["requires"] not in inventory:
            msg = f"You need a {option['requires']} to access this area."
            sleep(2)
            navigate_location(current_location, turns_taken)  # Return to the same location

        msg = f"You chose: {option['description']}."
        next_location = option["next"]

        # Check for a random encounter
        if random.random() < encounter_chance(turns_taken):
            random_encounter()  # Call the encounter function
            
            # Check if the player died during the encounter
            if not zombification() or game_over:
                return  # Exit the function if the player is dead

            sleep(1)

        # Continue to the next location
        navigate_location(next_location, turns_taken + 1)
    else:
        msg = "Not a valid input. Try again."
        sleep(1)
        # navigate_location(current_location, turns_taken)


def random_encounter():
    global player_hunger
    global playerzombi
    global survivor_count
    encounters = [
        "A zombie jumps out at you!",
        "A zombie attacks you!",
        "A zombie rips off one of your fingers",
        "You find a mysterious item on the ground.",
        "A group of survivors approach you cautiously.",
        "You hear a distant scream and feel uneasy.",
        "You stumble upon a trap!",
        "Bandits ambush you!",
        "You find some medicine.",
        "You encounter a frightened survivor.",
        "You lose your grip and drop an item."
    ]
    encounter = random.randint(0, len(encounters) - 1)

    if encounter == 0 or encounter == 1:
        
        damage = random.randint(1, 3)
        playerzombi += damage
        print(f"{encounters[encounter]} You take {damage} damage and feel the infection spreading!")
    
    if encounter == 2:
        
        damage = random.randint(2, 4)
        playerzombi += damage
        print(f"{encounters[encounter]} You take {damage} damage and feel the infection spreading!")

    elif encounter == 3:
        add_to_inventory("Mysterious Item")
        print("You found a mysterious item and added it to your inventory.")

    elif encounter == 4:
        survivor_count += 1
        print(encounters[encounter])
        print("You manage to gain another survivor!")

    elif encounter == 5:
        print(encounters[encounter])
        player_hunger -= 1
        print("Your hunger increases as the uneasiness settles in.")

    elif encounter == 6:
        damage = random.randint(1, 2)
        playerzombi += damage
        print(f"{encounters[encounter]} You lose {damage} health!")
        if "Bandages" in inventory:
            inventory["Bandages"] -= 1
            print("You use a bandage to stop the bleeding.")
            if inventory["Bandages"] == 0:
                del inventory["Bandages"]

    elif encounter == 7:
        if inventory:
            stolen_item = random.choice(list(inventory.keys()))
            print(f"{encounters[encounter]} They steal your {stolen_item}!")
            del inventory[stolen_item]
        else:
            damage = random.randint(1, 2)
            playerzombi += damage
            print(f"{encounters[encounter]} You have nothing to steal, so they attack instead! You lose {damage} health.")

    elif encounter == 8:
        add_to_inventory("Medkit")
        print("You found medicine and added it to your inventory.")

    elif encounter == 9:
        survivor_count += 1 if random.random() < 0.5 else 0
        if survivor_count > 0:
            print("You encounter a frightened survivor and they join your group.")
        else:
            damage = random.randint(1, 2)
            playerzombi += damage
            print("You try to help, but things go wrong. You lose some health.")

    elif encounter == 10:
        if inventory:
            lost_item = random.choice(list(inventory.keys()))
            print(f"You lose your balance and drop your {lost_item}. It is gone forever.")
            del inventory[lost_item]
        else:
            print("You stumble but don't lose anything as you have no items in your inventory.")

    # Function to determine the chance of an encounter
def encounter_chance(turns):
    base_chance = 0.4  # Initial chance of encounter
    max_chance = 0.9  # Maximum chance
    return min(base_chance + (turns * 0.05), max_chance)

clear()
def prompt():
    print("\t\tWelcome to Magic Zombie Land!!!\n\n")
    print("\t\tControls:\n\n")
    print("\t\tPress 'B' to use Bandages - Heal 1HP\n")
    print("\t\tPress 'M' to use Medkit - Heal 2HP\n")
    print("\t\tPress 'R' to eat Ration - Fill 1 hunger\n")
    print("\t\tPress 'F' to drink Fasting Potion - Fill 2 hunger and pay respect\n")
    input("\t\tPress enter to continue...") #input with no use will pause the continuation until user input
    clear()
# def journal():
    # print("\t\tJournal\n\n")
    # print("I don't know what's happened.\n Everywhere I look, I see people scared, running for their lives.\n All I hear is a mix of screaming and these eerie crackles of fear.\n Zombies.\n Zombies are everywhere, chasing after people down every street.\n I don't know how I am going to get back to my family.\n My son was at school, last I remember.\n My wife was at work at the museum.\n I hope I can get to them quickly.\n I need to get them to our home safely.\n Our home is on Abberley Drive.")
    # input("press enter to start game..")
    # clear()
prompt()
# journal()
hunger()
start_game()
navigate_location()
    # Function to navigate between locations


        
    # Main game loop, starting with the landing room IMPORTANT!
turns_taken = 0
navigate_location("landing_room", turns_taken)

