# Strava to LED Matrix
GitHub: https://github.com/jacobrkerstetter/StravaAPI 
Presentation/Demonstration: https://youtu.be/XuOWSsBUH-0 

Design Overview:
The goal of my project is to combine a hobby I am very passionate about, running, with my future career in software engineering. Thus, my Strava widget was born. This final product did not come without many revisions and iterations, but in the end created a jumping-off point for a very useful iOS widget as well as taught me valuable skills I was interested in learning. 

Strava is a fitness app that combines statistical tracking features with social media elements. For example, a user can post their runs, bike rides, and even racquetball sessions and view paces, durations, distance covered, and heart rate data. Additionally, users who follow them can give “kudos,” which are the equivalent of a “like” on other social media platforms. Strava has a well-built API to access data from a user’s account as long as the account has authenticated the API access. My initial goal was to allow a Strava user to view their most recent activity and key data on an LED matrix that they can display in their home. This eventually iterated into visualizing the activity on the home screen of an iPhone. 

The LED matrix idea came from a project I saw online a couple of years ago that utilized Spotify’s developer API to create home decor. The project displayed the current song title and album cover in full color on an LED matrix and updated live as long as the music-playing device was connected to the same WiFi. This project from SparkFun gave me instructions on the hardware I would need to physically implement my design, and my task was to develop the software and integrate them together. 


Figure 1. Spotify Album Art Demonstration
(https://learn.sparkfun.com/tutorials/live-spotify-album-art-display/all)

My final design ended up being an iOS widget developed in xCode. The widget displays the most recent activity with key data including distance and duration. With this fully software project, there is immense room to expand my project in the future, which will be discussed later. The rationale for this switch from hardware and software integration to a fully software project will also be discussed in the next section. Overall, the project still serves as a useful tool in my training as well as an aesthetic design to liven up the home screen of my iPhone. 


Figure 2. Apple iOS Widget Example
(https://www.macrumors.com/2023/04/12/ios-17-interactive-widgets-rumor/)

The justification for this project being applicable for a 6-week development period comes from a combination of my previous knowledge and work with some of the technologies I used in conjunction with the amount of new technology I needed to learn. For example, I am already an intermediate to advanced Python programmer and have used Python many times to interface with 3rd-party software via API’s. Contrasting this was my inexperience with hardware, specifically the LED matrix. Once the LED matrix was tested and failed, the contingency plan that was put in place was activated and I pivoted to another new technology: iOS app/widget design. This required me to learn Swift and SwiftUI, two languages I have minimal experience with. Although this felt daunting in a now shortened development period, I saw it as a great learning opportunity to boost my resume by becoming a beginner Swift developer as well as deciding if frontend software is a path I would be interested in pursuing in the future. 

Preliminary Design Verification:
To begin my design verification, I started with the technology I was most familiar with: Python and API’s. For a proof of concept, I wanted to pull data from my Strava account using the Strava API. Initially, I attempted to use Strava’s documentation for authenticating and accessing my account, but this proved difficult, as I was constantly losing privileges. After doing more research, I found that another developer had created and published a free Python module wrapping the Strava API with easier interfacing called “stravalib” (https://github.com/stravalib/stravalib).


Figure 3. stravalib Installation


Figure 4. stravalib Documentation on Git-Hub

After finding this module, I was able to easily authenticate my account. Please reference Appendix A for a walk-through of authenticating your account or for information on how I authenticated mine for this project.

Once I was authenticated, the next step was using stravalib to read my latest activities and print them to the terminal. For this step, I modified code from another GitHub user who had already done a similar task. This code can be found at the following link: https://github.com/anthonywu/strava-api-experiment/blob/master/src/strava_local_client.py. This link provides the framework for the getAccess.py file referenced in Appendix A. Code from another user was used as a jumping-off point for accessing activities, but I added much more functionality to it (https://github.com/barrald/strava-uploader/blob/master/uploader.py#L225). Figure 5 demonstrates my test of reading the most recent 5 activities from Strava and printing them to the screen.


Figure 5. Printing Activities from Strava

Stravalib provides the get_activites() function with a parameter to limit the amount of responses from the API. Here I used 5 as a test limit. The next step was testing a live update. The procedure for this was to put the above code in a “while True:” loop to constantly poll Strava for new activities uploaded to my account. 

The first finding from this test was that Strava has a rate limit on how many times you can request data. The limit is 100 requests per 15 minutes, up to 1,000 requests per day. To stay within this limit, I put a statement for my program to sleep for 6 minutes between every request. This is an ample amount of time to avoid the Strava timeout while providing a user with nearly instantaneous updates after they record an activity. This test was successful.

The final test to prove my project's validity was to ensure I could parse and write the necessary data to a .JSON file, a common file type similar to a Python dictionary for reading and writing data with API’s. My goal for the test was to write the activity name, distance, and duration to the JSON file. The figure below shows the resulting output format which can be indexed by category.


Figure 6. JSON File Output Format

Once I was able to complete this validation, I was confident in the software and API interfacing aspect of the project, and I moved to the hardware validation stage.

The hardware that I needed to validate was the LED matrix as well as the SparkFun ESP32 Thing that would be controlling it. The ESP32 Thing is a wifi-compatible microcontroller with nearly 30 I/O pins. The goal of the test was to wire the matrix to the microcontroller and run test code on it to ensure I could write to the matrix. The ESP32 runs Arduino code, which is a development platform I am familiar with. The tutorial from SparkFun utilized a library called PxMatrix.h which I decided to remain with. This library contains many function calls for drawing to the matrix as well as demo code to run. After many tries at writing to the matrix, the only output I was able to achieve was random red and blue lines. I checked my IO connections to the microcontroller and tried a few different power adapters, all conforming to the documentation of the LED Matrix, to no avail. After numerous failed attempts, I decided in the interest of time to go to the contingency plan: a fully software approach.

The original software approach was to use a module in Python called PyQt which can be used to create Python GUI’s and provide “signal” objects to update them live. This was a module that I had used in a previous class, and I was interested in learning a new skill in this project. After speaking to TA Joe, we agreed Swift and SwiftUI for iOS design was a relevant skill to learn as my career interests are mostly software-based. Designing an app would be redundant in this case as Strava is already a very well-made app. A widget is provided by Strava, however, it does not offer very much functionality – it merely displays your weekly mileage and mileage per day. My widget sought to provide more of an activity-focused insight to a user. Overall, this plan would still allow me to learn a relevant skill, although software-focused, as well as practice my software development skills.

Design Implementation:
I will first describe the block diagram of my original design with hardware and software integrated together. The initial idea was to create my Python client which can post GET requests to the Strava API, which would then in turn query their database. The database then responds with the requested data back to the API. Then the API returns the data to the Python client as a JSON. In my case, the stravalib module converts the API data to custom object formats which are more simple to use.

On the hardware side, the Python client connects to the ESP32 Thing via WiFi, where the ESP device is running a local server. The ESP receives the data from the client and is able to translate it to the LED matrix pins using the PxMatrix.h library. This design ultimately ended up failing, but the block diagram can be seen below.


Figure 7. Original Block Diagram

After the contingency plan was put in place, the block diagram transitioned to what is seen below in Figure 8.


Figure 8. Revised/Final Block Diagram

The subcomponents of this design are the Python client, the Swift class, the widget, and the Strava API. The Python client is responsible for the communication to the Strava API as before, but now also converts the useful information to JSON format and sends it to a .JSON file. The user.swift file creates a Swift class to read the .JSON file and parse the data into class members. The widget then interprets the data from the class to visualize it. 



Design Testing:
My test plan for my prototypes was to utilize what I have previously discovered and developed in the design verification stage as a starting point. Then, each iteration I do to my design can be done by changing one variable at a time, verifying it has the desired effect, and committing the new working code to GitHub. 

The first tool I used to test my prototypes was the .JSON file. This file served as a textual representation of the data I am pulling from Strava’s API and the way that I parse it. For example, one piece of functionality that I added was formatting of time strings for the duration of the activity. By default, if the activity is under an hour, Strava outputs the time as “0:xx:xx” in the format “hrs:mins:secs.” I chose to only display the minutes and seconds if the duration was less than an hour, so I removed the first two characters in this case and did a test output to the .JSON. This can be seen in Figure 6 above.

After testing these textual outputs, I moved to the visualization of the prototype widget. Below in Figure 9 is the first prototype I created. As is evident in the image, the data was not being correctly displayed – the duration and distance were both showing the distance. 

Figure 9. First Widget Prototype (Incorrect Data) with Strava Screenshot

While this was a step in the right direction as this is accurate data from my Strava account, the time did not display. After I fixed an issue in the code, I was able to display the data correctly, which is shown below.

Figure 10. First Widget Prototype (Correct Data)

As mentioned previously, authentication was a tricky process for me initially. After digging through documentation and many days of trial and error, I was able to successfully authenticate. This led me to develop Appendix A, which will hopefully serve as a useful instruction guide for anyone attempting similar projects.

On the SwiftUI front, styling proved to be the biggest challenge for me. As I will discuss in the future work section, this is an area that I would like to improve upon massively to make my project usable for the public. For example, I needed to learn the .padding and .resizeable attributes for images and text to align them better. The Spacer() function was also useful for this task. 


Figure 11. Second Widget Prototype

Figure 12. Third Widget Prototype

Summary, Conclusions, and Future Work:
All in all, creating an iOS widget for a topic I am very passionate about was a great learning experience as well as a resume bullet point. I was able to learn the basics of Swift, SwiftUI, and JSON file processing while practicing my neglected Python and API skills. 

Some conclusions I came to while completing the project were that if I had a longer development cycle, I would have likely been able to get the hardware to work. This could be placed in the category of future work for the project. 

One element of future work that I identified that I am highly interested in is deploying my Python code to run via an AWS or Google Cloud service. This would free up my personal resources and refresh the widget automatically. Although this is seemingly simple, it would require the posting of a finalized version of my app with generalized functionality to allow it to not only run my Strava data but be individualized to any user that wants to download my widget. This would be a good exercise is app deployment but is beyond the scope of this project’s timeline.

Additional trivial future work includes UI improvements. As this is my first time using SwiftUI and making a widget, my design skills were lacking. In the future, I would be interested in collaborating with an advanced SwiftUI designer to boost the aesthetics of the widget. This also includes a more seamless integration with iOS with typography, shapes, and color themes. Although there is future work to be done on the prototype to polish it into a production-level widget, I am pleased with the output I achieved, and I hope to work to develop more running-related products in the future.
Appendix A: Authenticating Strava for Your Account
Clone the repository into the desired drive with the following command:



Figure 5. Cloning the Repository
Create a Strava developer account by going to https://www.strava.com/settings/api and registering. This will display a Client ID and Client Secret. These are private keys that need to be kept hidden, but known to yourself. I put them in a file called client.secret. This would be a good case to use a .gitignore file with the condition “*.secret” to ignore all files of .secret type. Below is what the Strava page should look like to find the Client ID and Client Secret.


Figure 6. Finding the Client ID and Secret

Now you can run the getAccess.py file using the ID and Secret as command line arguments to open an authentication page. The following is the command. Replace the bracketed elements with your information: 
python3 getAccess.py get_write_token <client_id> <client_secret>
Once the webpage has opened, you click the authenticate button and a blank page will pop up with a long code in the top left. Copy that code and paste it into the getActivities.py file or add it to your environment variables. I recommend adding it to the file directly.

Figure 7. Getting the Authentication Code for Strava
