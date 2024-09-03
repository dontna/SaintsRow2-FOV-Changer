# SaintsRow2-FOV-Changer
A Python script that allows you to set a custom FOV in Saints Row 2 PC

# What does it do?
The script modifies the 'custom.vpp_pc' file to allow you to set a custom [Field Of View](https://en.wikipedia.org/wiki/Field_of_view_in_video_games) or FOV for short. This is usually useful for people who play on resolutions not natively supported by the game such as 3440x1440, however anyone can get use from this.

Here are a few images, that show the difference.

Before FOV Changes            |  After FOV Changes
:-------------------------:|:-------------------------:
![interior_before_edit](https://github.com/user-attachments/assets/27f2a1a6-3049-4f45-97d2-477897f507cd) | ![interior_after_edit](https://github.com/user-attachments/assets/13b5e422-7cf7-4020-98e3-8b3ad39a4bcd)
![outside_before_edit](https://github.com/user-attachments/assets/c894f0f6-0fb6-454e-a4f5-e415685adee7) | ![outside_after_edit](https://github.com/user-attachments/assets/46c54b1b-ad3c-450e-8be2-bda0e9f589f7)
![driving_before_edit](https://github.com/user-attachments/assets/4f28522f-c1bc-456d-a52b-b4f31d971b95) | ![driving_after_edit](https://github.com/user-attachments/assets/995042ea-9744-4666-a280-cea78255312a)

In the screenshots I am using the resolution 3440x1440. The FOV settings were a result of using the **gset** command with a modifier of **1.25**.

# Setup
If you don't have it already, please install Python otherwise the script will not work. 
  * If you're on Linux, it should be installed by default; so you should be good to go! 
  * If you're on Windows, it will not come pre-installed so you'll need to download it through the [Windows Store](https://apps.microsoft.com/search/publisher?name=Python+Software+Foundation&hl=en-us&gl=US).


Before we run the script, I recommend adding your game path to the 'SR2Fov.ini' file. While this step is optional, if you do not do it you'll have to manually give the script the path to your game folder each time you use it.

Follow these steps to add your game path to the 'SR2Fov.ini' file:
  1. Open your Saints Row 2 game folder
      * If you're on Steam, here's a [super quick video](https://www.youtube.com/watch?v=_ETOk98WN1A) on how to do this. They use Grand Theft Auto V, but you just have to choose Saints Row 2, and follow from there!
  
  2. Copy the path from the bar
      * If you're on *Windows 11* you might have to **Right Click the bar** --> **Copy address**

  3. Open 'SR2Fov.ini' in a text editor, and add the path you copied.
      * Make sure the path is wrapped in quotation marks ( " " ), otherwise it may cause issues in the script.

  Here's how it should look:

  **Linux**
```
[PATH]
GameDirectory = "/mnt/games/SteamLibrary/steamapps/common/Saints Row 2"
```
  **Windows**
```
[PATH]
GameDirectory = "D:\SteamLibrary\steamapps\common\Saints Row 2"
```

Our paths probably won't look identical, but this is a gist of how it should look!

Now you can save the file, and you're done!

# How to use?
Now we've completed the setup, you're ready to run the script 'fov_fix.py'.

  **Linux**
  `python fov_fix.py`

  **Windows**
  `If Python is installed, you should be able to double click on the file to run it.`

If your path is correct, you should see a list of FOV options you can edit
```
0. General FOV
1. Sprinting FOV
2. Interior FOV
3. Interior Sprint FOV
4. Fine Aim FOV
5. Human Shield FOV
6. Vehicle Passenger FOV
7. Land Vehicle FOV
8. Boat Vehicle FOV
9. Helicopter FOV
10. Airplane FOV
11. Swimming FOV
12. Climbing FOV
13. Ragdoll FOV
14. Falling FOV
15. Freefall FOV
16. Parachute FOV
17. Fireworks Truck FOV

Please type a command or 'help' if you need a list of commands: 
```

It may look a little confusing, but it is quite simple. The number next to the text is the category number, the text is just there so you know what each category is for. If you're still confused you can type the command `info` followed by a category number to see a description about the category.

As an example, let's say we are confused about `17. Fireworks Truck FOV`, we can use the info command to give us a description like so `info 17`, once we press enter we will see the following description `Fireworks Truck FOV --> This is your FOV while in the back of the fireworks truck in the mission "Thank You and Goodnight!", it is not used for anything else.`

Now we know this FOV value changes the FOV when using the Fireworks Truck crates in the mission [Thank you and Goodnight](https://saintsrow.fandom.com/wiki/Thank_You_and_Goodnight!)

All of the commands follow a similar pattern, but if you're ever confused you can type `help` at anytime to show a list of commands, their usage and a description.
```
help
     description: Show this message
     usage: help 

info
     description: Show a brief message about a category
     usage: info [category_number] 

get
     description: Get the FOV value for a category
     usage: get [category_number] 

set
     description: Set the FOV for a category
     usage: set [category_number] [new_fov_value] 

gset
     description: Globally set all FOV values based on a multiplier.
     usage: gset [float_multiplier] 

reset
     description: Set all FOV categories back to their default values.
     usage: reset 

load
     description: Load FOV values from the 'SR2Fov.ini' file
Note: The SR2Fov.ini file must be in the same directory as the script.
     usage: load 
```

As a final example, let's set an FOV value for a category. How can we do this?
1. Choose the category we want to change
    * in this example, I want to change the `0. General FOV`

2. Use the `set` command to set the value
    * I want to set the General FOV, to 80. This is what it would look like in practise `set 0 80`
        * `set` is the command
        * `0` is the category number
        * `80` is the new FOV value`

3. Press enter and our FOV value will be written to the file instantly.
    * as long as all parameters are valid, you should see `Sucessfully set General FOV to 80`

Once you've made all of your changes, you can exit the script by typing `exit` or `quit`

The next time you load into the game, the FOV will be changed!


# Update
As of the **3rd September 2024** the script can now handle three-digit FOV values, meaning you can set your FOV to anything between 1 and 999. Realistically the "limit" is 180, because after that your FOV can become unstable and glitchy; but feel free to use any values you want.

Here's a photo of me in game, using 160 FOV
![Screenshot_2024-09-03_16-33-41](https://github.com/user-attachments/assets/c23c992b-0315-4e33-9ebc-5a14a61ac34b)
# Forking my work
You are free to take this script and make it your own.
