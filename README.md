# WORKOUT! Web-App
#### Video Demo: https://youtu.be/xHBzPLzAve8
#### Description:

This is a web-application with features such as,
BMI & Waist-Hip-ratio calculator to let users have some insight into their health status,
IntervalTimer for HIIT, Tabata and whatnot,
Stopwatch to keep track of time elapsed, AND
Workout plans which enable users to personalise.
The webapp has built-in workout plan and some exercises for user to customise plan themselves. The users could also update their choices of exercise.

The web-app is loosely based on CS50 Finance in terms of use of Flask and some idea of styling (Navbar). In terms of styling, I have implemented Bootstrap. The webapp is designed to fit in all devices.




**The Registering and Loging In**

The users are required to create at least a 8 characters password with letters and numbers only with at least a number in it.
The checking of inputs and password are done on the client-side, the user won't able to submit until all requirements turn green. The username is checked from database after submitted.

For login, the submit button is only enabled when both fields are input and the password has more than 8 characters.

Both pages will return back when there are invalid username or incorrect password.


**The Home**

Home page can be redirected when the "WORKOUT!" is clicked. Both calculators stay here. The BMI calculator will show the health status based on the value calculated, while waist-hip-ratio calculator shows only value but the healthy range has been stated on page.

**The Interval Timer**

The users first set the duration, break and repetition. Essentially, the timer is ran with `setInterval()` methods in Javascript. The innerHTML will be updated when the timer is running.
When the workout is completed, the workout info is sent to database through url.


**The Stopwatch**

The stopwatch is quite similar to timer in term of the `setInterval()` methods in Javascript.
When the workout is saved, the workout info is sent to database through url.


**The Workout Plan**

When a existing plan is choosen, the user is redirected to start.html to have a view on the workouts in plan and a start button to start.
When the workout is completed, the workout info is sent to database through url.

When the user chooses to create new plan, the user is redirected to createPlan.html, user could search for workout with asynchronous search bar and select dropdown for catogeries. I have made the search result to return in JSON and insert each as table row for view.
The user could adds, deletes, sets duration and break time to create a new plan. To create the plan, I decided to send formdata to server as my solution, I had stringify the array of workouts and append into the formdata so that all informations of the plan will be received bu server.

Besides, there is also feature for user to add new workout for more workout options when redirected to addExercise.html.


**The History**

Show users their workout histories ordered from latest. The histories will also display the duration and the name of workout.




**Room for Improvement**
1. Publish in Heroku.
2. Sound effects, BGM and short description for workout
3. Back button for create plan and add exercise
4. Users' info page
5. Statistic of users' weight and etc