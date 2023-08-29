# World Of Humour App
#### Video Demo:  https://youtu.be/0RYcQ4_ow24
#### Description:A Personalized Web App returning jokes to the user

My idea was to help a bit with the log hours in coding, instead of going to scocial media for a quick distraction I wanted to build something that didn't distact you in a way that its difficult to get back into your code space.

So I developed WORLD OF HUMOUR.

A web based app that return jokes and allows you to create a profile and adjusts according to certain details your entered like gender and age.This web app enables you to select the categories of joke you want to recieve aswell as give you the option to choose restrictions on topics that should be avoided.


1 **LOGON PAGE**
The logon page is relly simpel it creates an effect of unlocking the app and take you to the login page

2 **LOGIN PAGE**
The login page consits of a form that animates into the viewport and give you an option to click the register button and go the register route.
The form has an action called post and goes the login route.The details entered here will be verified against the data in the data base and will deny you acces to the home screen if you entered it incorrectly.

 **REGISTER PAGE**
The register page consists of a form where you wil be filling in your details into the given fileds.The data will be entered into a database.After the resister button is clicked you will be taken to the login screen.

4 **INDEX PAGE**
Index page cosists op a welcoming message and a header where you can click or hover on and see a create profile button where you will be given the opportunity to create a profile.

**PROFILE PAGE**
Here you can enter the rest of your details and also a profile picture that will show on your profile the whole time through when your are using the app.Depending on the gender and age entered the home screen and options to access certain topics will vary.

**HOME18 PAGE**
This page is for the younger audience.It defaults to hiding the options to access certain topics of joke like sexist, religious ect.
The background will aslo vary on the gender entered for example a male will have a different background image than a female.
This page consists of a few div boxes with some checkboxes to be selected and passed to a function upon the get Joke button is pressed.
Here you wil be able to select the categories of jokes you want to receive aswell as the ones that should be avoided.You can also choose different type of jokes, for example "twopart" or "single"

**HOME18+ PAGE**
This page is similiar than the HOME18 page except that this page has a few extra options because op the fact that you will be shown this page after entering an age above 18 years. Again the background will vary depending on the gender entered.
The pages consists of a few div boxes with checkboxes whose values are passed to a function when the "Get Joke" button is pressed.
Here you wil be able to select the categories of jokes you want to recieve aswell as the ones that should be avoided.You can also choose different type of jokes example "twopart" or "single"

**JOKEHOME PAGE**
This page will display to you the twopart jokes. The values passed to the function via the checkboxes will query the API and be diplayed in div boxes with a "Refresh" button and you will still have the same background that was given to you because of the the age and gender values.

**JOKEHOME1 PAGE**
This page will display to you the single jokes. The values passed to the function via the checkboxes will query the API and be diplayed in div boxes with a "Refresh" button and you will still have the same background that was given to you because of the the age and gender values.

**THE LAYOUT TEMPLATE**
This page just contains the structure and all the imported libraries that was use in this web app.

**STYLE.CSS**
This is just the styling for the web app to make it responsive aswell as make it look presentable. I used some media queries to make sure everyting lines up correctly when the screen sizes differ.
There are also a few animations that was used to make elements animate into the viewport.

**UPLOADS**
This file is where all the uploaded profile photos will be strored and the opened and read as binary to insert it into the database.

**APP.PY**
This file is where all the functions are defined when you access certain routes via the app.
This file will also query the API, store your user id into a session variable and contain all the other logic and libraries needed to make the WebApp.

This file will also be responsible to insert the data entered into the database using sqlite3.
Because of the Web App and some image files being really large this file will also contain a compress function where some contents will be compressed when its larger than a certain size.
The rest is just sanitizing the data entered and checking is the data entered is correct and return an output acording to that.
This file also encodes the image files that will be quried form the database in binary and the passed through jinja to the template where it will be decoded and rendered.

**USERDATA.DB**
A data base where the information will be stored that was entered that consists of a few rows, one of them that has BLOB format to store the uploaded image.
