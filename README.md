reporting
=========
AIM:
===
"Made to  relieve poor online community manager 
that copy paste every day simple stats on their favorite social network.
No, there is no need to authenticate or to use API" 

===
Simple script for reporting social media performances such as Facebook, Twitter, Instagram:
Convert social metrics into:
JSON
HTML
and can be send by mail as RAW TEXT or graph

===
HOW DO I RUN IT?
1. create a csv file called "report.csv"
2. add into the report.csv the url of the webpage (facebook, twitter, instasearch): one url by one line s shown in example report.csv
3.Into main.py: 
add the type of report you want:
-HTML/CSV/GRAPH
add the options for mail
-FROM, TO , TITLE OF THE MAIL
4. into a CRONTAB for routine:
m h  dom mon dow python report/main.py 
And that's all!



