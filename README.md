
# UNOFFICIAL CYBERPUNK 2077 BUILD CREATOR 

This software is an Unofficial, Fanmade Desktop app for Windows created by Cris, going by usernames such as AnybodyC, Crips or Crispy.
This app allows it's users to view, create and modify custom build plans for the game Cyberpunk 2077.
After creation/modification, a file receives a code. This file can than be saved or opened and the code can be copied or entered into (another instance of) the app.


# TABLE OF CONTENTS 

- Installation
- Unincluded Components
- Usage
    - Attribute Screen
    - Cyberware Screen
    - Weapon Screen
    - Stats Screen
    - Sharing
- Configuration
- The Creation

# INSTALLATION 

In order to use the program. The user has to either 
A)  Open the .exe file (recommended)
or 
B)  Install PyQt5 and run the main.py file in a terminal. Opening the entire folder in the terminal may be required. Some work on the directory path may also be required.
For both of these methods a stable version of Python (at least 3.6, preferrably 3.11 or 3.12) is required.

# UNINCLUDED COMPONENTS

Phantom Liberty Relic Perks are not included in the build creator, as they mostly only provide gameplay alterations, as opposed to stat alterations. 
Generally, the Headshot stat may be taken for Weakpoints as well.

Quickhacks themselves are not included, as their damage and effects vary wildly depending on previous Quickhacks used and/or Targets and/or Situation.

Silencers and such are not included. Given the Headhunter skill bonus of stealth effects staying active shortly after being detected, it's accepted that each weapon could benefit from stealth bonuses from perks and/or cyberware, and thus those bonuses show up for those weapons in the stat screen.

Throwing knives and axes are kind of strange in damage calculations. With these weapons, the DMG stat indicates the damage displayed with the weapon, but the DPS stats include a x1.5 multiplier for the weapon being thrown. 
In game, this multiplier will most likely be much higher, though in calculations, I couldn't locate a precise multiplier for the weapopn being thrown, thus I am leaving it at x1.5.
So, for throwable weapons, note that the damage calculations are off, and that the best way to use this tool for throwables is for comparison with other throwables in the same tool.

# USAGE

##      ATTRIBUTE SCREEN
In the Main Attribute Screen it shows 2 layers. 
    The Top Layer shows each attribute and their level, the "+" and "-" buttons allow you to change the values of the attributes.
    The Bottom Layer shows each Skill type and their bonuses, as well as what progresses this Skill stat's level
Pressing one of the "PERK POINTS" buttons will navigate you to the Perk Selection Screen corresponding to the Attribute the button belonged to.
This screen consists of a grid. Generally, each slot in the grid consists of a main "Node" perk, and it's subperks. These Nodes correspond to the main perks in the in-game skill tree, and the subperks are all the perks connected to the node.
This is not the case for the "Special" perks, which are the perks in the (bottom) right, indicated by the green names. This grid slot contains the vehicle perk for the attribute, as well as all the level 20 perks. 
Hovering over a perk will show the specifics of the perk, being the description, what weapons are affected by it, etc.

Generally, when a perk is the same colour as the darker background, it is unavailable to unlock (this is sometimes not the case with perks that have dependencies outside of their grid slot).
This can be due to the attribute level not being high enough, or because some other perks are not unlocked yet.
When the perk colour becomes the same as the background of the grid slot, it is also generally available to unlock.

In Phantom Liberty, the maximum amount of attribute points that can be acquired is 66 points. The maximum amount of perk points is 80. Theoretically, these limits can be circumvented by combining or altering the shareable codes, though this is discouraged (code might just not work). Read more in the SHARE section of Usage

##      CYBERWARE SCREEN
The Cyberware Screen contains 4 columns, the 1st and 3rd being the ones showing the cyberware currently equipped, the 2nd one sporting our favourite edgerunner and displaying the cyberware cost and armour. The 4th and rightmost column is for selecting new cyberware.

Empty slots are noted by the blue shape with "CYBERWARE" inside. Clicking on one of the slots will open the Selection menu and allow you to scroll through the cyberware available in that slot.
Click on the image of the cyberware to add it to your selection.

A few important things to note for this:
- The current selected slot gets a small blue border around it. Note that specific slot locations do not transfer when reloading the page, meaning that picking the 3rd slot will just return it to the first when reloading the page.
- While there can never be 2 of the same cyberware in a build (except through code altering), there can be an Iconic version and a non-Iconic version in a build at the same time. It's quite simple, the game does not allow 2 Cyberware with the same icon.
- The cost displayed when scrolling through the cyberware is the absolute cost, and is not reduced by any cost reducing perks. The Yellow Cyberware Cost number below David does account for these perks however
- The armor given when scrolling is also the absolute armor, it is not increased by Armor %-increases, attunements, or any perks or skills. To view the final armor, go to the Stats Overview

In the selection, hover over a selected cyberware to view it's description, name, etc..

##      WEAPON SCREEN
This screen consists of 3 Areas. The leftmost area is where weapons will show up when selected. There are 4 slots, the 4th being to select a weapon and compare them to the ones that are in one of the first 3 slots. This slot is contains a special "Comparison/Extra Slot" text at the top.

In each area there are 4 spaces. The 1st contains an image of the currently selected weapon. The second contains the name, type, weapon type and the DPS counts.
A few things to note on the DPS counts:
- DPS Low is calculated using a 'simple' DPS formula that uses damage, attack speed, reload time and magazine size. This formula can be viewed by hovering over the text "DPS Low"
- DPS High is simply DPS Low * Headshot damage increase, this can also be viewed through tooltip.
- The No Reload stat is simply Damage * Attack speed * Headshot damage increase
- Blade, Blunt and Throwable weapons use different formulas, these can all be viewed by hovering over the DPS text.

On the bottom left of a slot, it will display the Iconic and Intrinsic modifiers for a weapon. Again, you can hover over these to fully display them, in case they get too big for the slot.

In the bottom right, it displays the base stats for each of the weapons. Note that this stat still excludes any Intrinsic or Iconic modifiers.

In the middle, there is a thin column with several buttons.
The Yellow buttons are all Weapon Types. Any buttons that are yellow signify weapons in the weapon Types that are in the selection. When none of the buttons are Yellow, all of the weapons are active.

Below, the blue buttons are all sorting options, when no weapons are added via the buttons, it is a basic selection, adding more types will add more sorting options. Sorting takes place using mergesort. This and creating all the labels for all of the weapons might take a while. Sorting by a sort option that not all weapons in the weapon type selection have will result in those weapons being removed from the selection (though only for that specific sort option)


All the way on the right the Weapon Selection Screen will appear. Each weapon contains the image, name, type, Iconic and Intrinsic modifier, as well as the stats. Each of the stats has a color from red to green. The greener it is, the higher it is above the average. The average is calculated from all weapons currently in the selection that also have that stat.


## Stats Screen
In the top right, it displays 4 buttons. Clicking these can turn the bonuses from those categories on and off.
More on these buttons:
- Perks - Perks contains bonuses from all of the perks, but also from the attributes. 
- Skills - Skills contains bonuses from the skills (visible in the bottom row of the attribute screen). When On, they are all active, when off, none are.
- Cyberware - Cyberware contains all bonuses added by cyberware, being the effects, armor and attunements and anything else that might be connected to it.
- Weapon Icon./Intrin. - This contains the weapon Intrinsic and Iconic modifiers.

Below these buttons, there is a list of all the cyberware currently selected. Hover over these to view specifics.

On the bottom of this column, it displays 2 buttons. Low Stats and High Stats. Here is some more info on these:
- Low Stats contains any stat that is *always* active. For example, base armor from your cyberware is always active, the %-increases it might have based on certain effects is not. 
Another example, the first level of the focus skill is always active, the second level is not. Operating Systems like Sandevistan, Berserk or the Overclock from Cyberdecks, are not active.
This button can be used to view the baseline of a build, basically to view what the build is like at it's absolute worst. 

- High Stats contains *all* bonuses. Those that are *always* active, and those that have a condition that needs to be met to be active. *Note that conditions are not taken into account, for example, close range and far range bonuses can be active at the same time.* This, like Low Stats, presents a quite unrealistic view of the build. Sometimes, the %-increases cannot be reached, as 2 bonuses are mutually exclusive. However, the point of this is to show how good the build could be in peak condition (AKA when meeting all conditions for perks to be active), as well as showing all the bonuses that contribute to certain stats, not necessarily always active at the same time.

One can always view the current bonuses by hovering over a %-increase.


In the middle, the weapons are presented. Each weapon gets 6 stats:
- Damage - This is simply the base damage * (1+Percentage Increase)
- Attack Speed works the same as damage
- Crit Chance - Crit Chance is simply the percentage added, but capped at 100%
- Crit Damage - The Base Crit Damage is 50%, so this stat is simply 50%+the added percentages
- Headshot multiplier (Blades and Blunt weapons do not get this stat) - the final % is the weapon's base % + the % added from other sources (Weapon Iconics and Intrinsics counts as other sources) *Note that Headshot multiplier in damage calculations is (1+(HSM/100)), not (HSM/100).
- Peak DPS - The first stat would be the damage dealth when attacking at max speed and adding the average crit damage dealt in a second. However, this stat does not account for reloading. The second stat would be the first, but only hitting headshots. *Note, For throwables, the fire rate taken is 1, and a x1.5 throwable multiplier is applied, see UnIncluded Components for more.* Hovering over the second stat will provide a Tooltip containing the max damage dealt in a single shot.


The rightmost Column contains some of the other stats. The top segment contains the 'basic' stats, the middle segment the stats decreasing damage. The lower segment contains some stats for quickhacks and RAM regen.


Some bonuses are not included for calculations, often, this is included in the description for the bonus.
There might be some other cases like:
- Instant health regen effects are not included in Health Regen, including Healing Items. This is because it's kind really confusing to have to display infinite healing per second, depending on several other factors.
- Quick melee stats are excluded, they have no effect
- Some other stats with explainable reasons. 

# SHARE
In the top left of the screen, there are 3 buttons. Save, Open and Share.
These lead to these options:
- Save File / Copy Code - This option shows a code, copy this code and enter it in the Enter Code option to load it. You can also enter a name and then save to create file with the name you entered, containing the code.
- Open File - The files created by Save File (as well as a new file) can be loaded through this function, simply follow the options
- Enter Code - Enter a valid code, if the text entered is not valid, it will reopen the popup. If this keeps happening, please consider checking the code following the code syntax below.

## The Code Syntax
This is an example code:

*Bkm/30/+1t3Rk1i/60/u+1rjTk20/i/+1i+3u+3o2I30/7v/Ci0/7p/+1g+1p-114a319b2023b527a3237-34c924*

Each code consists of 3 parts, split by the "-" signs. 

The first part codes for the Perks and attributes. it starts with a letter, indicating the attribute, followed by a character. This character is a base-32 representation of the current level of the attribute. The characters that follow can be split into 3 again using the "/" signs<br>
The first part of this code is a base-32 number obtained by checking each node in a perk list, and noting which nodes are completely full by a 1, and the ones that are not by a 0. This creates a binary string, this string is converted to the base-32 number
<br>
The second part is the same, except for all the completely empty nodes.
<br>
The third part represents all the nodes that do not fall into the two categories above.
It is either a single character, or 3. If it consists of 3 characters, the first will be a "+" sign, the second 2 will be the base-32 representation.
<br> the base-32 representation of each node is created by first creating another binary string from all the perks in a certain node *(note that perks with a maxlevel > 1 take 2 binary chars to represent)*, and then converting this binary string to a base-32 number.

The Second part of the code is for Cyberware. This should *always* consist of 21 characters. Each character is a base-32 representation of the cyberware index for a certain file. The files are in alphabetical order and the amount of slots per file is the maximum that could be acquired in the builder.

The Third part is for the weapons. This should *always* consist of 6 characters. 2 for each weapon, the first character codes for the file index, the second for the weapon index in that file. '00' will code for 'Empty Weapon'. The fourth weapon slot in the Weapon Screen is not represented in the code.


# CONFIGURATION
Any perks, stats, images, whatever can be changed by finding the correct text file and changing the stats in that file. Syntax depends on the file it's in.

# THE CREATION
This is a completely Unofficial, Fanmade build editor. 

I, Cris, made this over a course of 2 months. Any Feedback is welcome!