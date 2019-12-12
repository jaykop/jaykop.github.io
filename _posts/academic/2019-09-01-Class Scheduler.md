---
title: "Class Scheduler"
excerpt: "A web based class scheduler for DigiPen students"
categories: academic
header:
  teaser: "assets/images/DigiPenScheduler_thumbnail.png"
---

<figure class="half">
    <a href="/assets/images/DigiPenScheduler_page1.png"><img src="/assets/images/DigiPenScheduler_page1.png"></a>
    <a href="/assets/images/DigiPenScheduler_page2.png"><img src="/assets/images/DigiPenScheduler_page2.png"></a>
</figure>
<figure class="half">
    <a href="/assets/images/DigiPenScheduler_page3.png"><img src="/assets/images/DigiPenScheduler_page3.png"></a>
    <a href="/assets/images/DigiPenScheduler_page4.png"><img src="/assets/images/DigiPenScheduler_page4.png"></a>
</figure>
<div style="text-align: center" markdown="1">
</div>

*Sep 2019 - Dec 2019*  
*By Webcake (Team of 3 programmers)*  
*ReactJS, Postgresql*  
*A web based class scheduler for DigiPen students*  

---
**Desciption:**  
<div style="text-align: justify" markdown="1">
&nbsp;&nbsp;&nbsp;&nbsp;This is a web application that helps DigiPen students set their semester class schedule. Students can simply see the visual timetable consists of classes they selected and much intuitive to check if there is time conflict between the classes. Hopefully, this application improves students' user experience at the beginning of the semester!
</div> 

---
**What I did for this project**  
  * Role: Programmer  
  * Parsed class Information from the database
	  - Send query to the database and receive the raw data
	  - Using knex, all the query language used are ported to use in JavaScript
	  - With given the data, it parses the class name, sections, rooms, days, professors, start time and end time of each session.
  * Checked time conflict between selected classes
	  - Using the parsed data from the parser, this feature compares two classes if there is any time conflict between them
	  - If there is a conflict it returns true, otherwise, it returns false
  * Generated all the possible schedules based on selected classes and remove a class from each schedule
	  - This feature handles all the combinations of classes, a schedule passed time conflict test, to add a new class and exclude one from the schedule
	  - Merging operator adds a new class to the existing schedules, check the time conflict, and then returns a new list of possible schedules that user can select
	  - Subtracting operators simply search the schedules that contain the class to be removed. Once it found a schedule, then remove it from the list of the schedules
  * Implemented test code
	  - All the codes described above; Class information parser, time conflict checker, schedule merge/subtract operator are tested using jtest. Tests have various edge cases and all those are covered by mitigation
  * Designed credit page and splash page
  * Using tailwind css, I implemented DigiPen logo splash screen at the beginning of the web application. Also, I added a credit pop up window by clicking a button on the right downside
  
