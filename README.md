
# gholder - SnapBot

Decription:

I made this app to do specific mouse actions for a certain amount of iterations based on predetermined mouse locations. The methodology behind it is to automate snapchat to give you whatever snapscore you want(Can increase it but can't decrease it). I'm currently looking into if there a way I can have this happen in the background while performing other actions with my mouse and keyboard while the program is running. Looking into switching to pynput, using a virtual machine, or selinum. Once I can automate this to the background I also want to create a website using Websockets to keep track and update to let you know on the GUI what snap you are currently on.
## Documentation

[Documentation](https://www.notion.so/SnapChat-Bot-Documentation-127a4ce68431806aba13e4f436f153fc?pvs=4)

Run command using:

```bash
sudo python3 [snapController.py](http://snapcontroller.py/)
```

### Important Notes:

Install frameworks and libraries:
Install pyautogui
Install tkinter
Install keyboard

- Once running make sure to enter the number of snaps you want to send, it won’t run until you do.
- To store points press the ‘Enter’ key.
- When app is open the ‘Enter’, ‘Ctrl’, ’Space‘, and ‘Esc’ keys all won’t work as they have new bindings.
- ‘Enter’ store mouse position points in your list
- ‘Space’ runs the auto clicker with the points you have saved
- ‘Esc’ stops the auto clicker
- ‘Ctrl’ quits the whole program

Behind the scenes it uses ‘pyautogui’ to perform the mouse clicker operations. It also uses the ‘keyboard’ library for the keyboard functionality. Keyboard functionality is built on the 

```python
keyboard.hook(on_key_event)
```

call. The UI currently uses tkinter grids to align all the elements, and show when states on the backend are being updated via keyboard input. Hotkey functionality is outdated and will be changed/removed soon.

‘targetSnapValue’ is initially set to 0 so the program won’t run if this field isn’t set. Potentially considering adding a UI component to display when the program is attempted to be ran when this field isn’t set.

## Demo

Run app using:

```bash
sudo python3 snapController.py
```
## Authors

- [@gholder513](https://github.com/gholder513)


## Important methods

#### record_global_clicks


##### This method gets the position of the mouse currently, and updates the GUI.


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `self` | `object` | The **SnapBot** object |

#### on_key_events

 
##### This method triggers every time a key is pressed.


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `e`      | `Event` | The key event observed by the keyboard.hook listener. |
