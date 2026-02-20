# ASD

This is a little guide I've made to help us understand the folder structures. 

## Models folder: 
represents the class diagrams. Each class in the class diagram should become 

```
class Repair
```
for the repair class, for example. It talks to the db.py and contrains the logic/calculations.

## Gui folder: 
 this represents the use cases and sequence diagrams

 each page has a tkinter form collecting user input, calls the model methods from the models folder, and displays results

 no sql, or calculations


 # SIMPLY

 when user clicks button, gui collects input, gui calls model method, model updates db, gui shows success message.

 ## git commands

 we are not going to be working on main. we want to work on our own branches until we've completed the testing. and then we will merge at the end. 
