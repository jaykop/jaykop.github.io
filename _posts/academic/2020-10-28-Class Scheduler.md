---
title: "Class Scheduler"
excerpt: "A web based class scheduler for DigiPen students"
categories: 
  - project
  - academic
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

*09/2019 - 12/2019*  
*By Webcake (Team of 3 programmers)*  
*ReactJS, Postgresql*  
*A web based class scheduler for DigiPen students*  

---
**Description:**  
<div style="text-align: justify" markdown="1">
This is a web application that helps DigiPen students set their semester class schedule.  
Students can simply see the visual timetable consists of classes they selected and much intuitive to check if there is a time conflict between the classes.  
Hopefully, this application improves students' user experience at the beginning of the semester!
</div> 

---
**What I did for this project**  
  * Role: Algorithm Programmer  
  * Implemented a ***parser*** which refines class Information from the database into numbers, strings
	  - Send query to the database and receive the raw data
	  - With given the data, it parses the class name, sections, rooms, days, professors, start time and end time of each session.
  * Developed a ***time conflict checker*** 
	  - Using the parsed data from the parser, this feature compares two class schdules if there is any time conflict between them
  * Built a ***schedule generator*** which provides all the possible schedules based on user-selected classes
	  - This feature filters invalid schedules out and returns possible combinations of classes
	  - Merging operator adds a new class to the existing schedules, checks the time conflict, and returns a new list of possible schedules that user can select
	  - Subtracting operator simply searches every schedule which contains classes to be removed. Once it found a schedule, then remove it from the list of schedules
  * Tested the features
	  - All the codes described above; Class information parser, time conflict checker, schedule merge/subtract operator are tested using jtest. Tests have various edge cases and all those are covered by mitigation
  * Designed credit page and splash page
    - Using tailwind css, I implemented DigiPen logo splash screen at the beginning of the web application. Also, I added a credit pop up window by clicking a button on the right downside
  
