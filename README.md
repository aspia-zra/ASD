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

 no one works on the main branch. we want to work on our own branches until we've completed the testing. and then we will merge at the end. 
 if ur creating ur branches for the first time, pull the latest main (do this once ever):

STEP 1: pull down overall folder structure
```
git checkout main
git pull origin main
```
STEP 2: create your own branch:

```
git checkout -b login-feature
git push -u origin login-feature
```
instead of login-feature, rename your branch

then u can commit and push normally. but make sure ur on git checkout [ur branch name], not main.













 
