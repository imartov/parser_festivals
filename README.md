# parser_festivals

This parser collects from the site https://www.skiddle.com
information about festivals and events held and returns
it in a convenient and sorted form.

All the code is presented in the file
https://github.com/imartov/parser_festivals/blob/main/parser.py.

Information about each festival contains:
- name;
- date of the event;
- venue;
- price;
- FAQs list.


<b>The first difficulty of parsing this
site was that festivals are loaded into
it dynamically using JavaScript:</b>
![image](https://user-images.githubusercontent.com/116018998/216822224-95d59986-bb83-430e-ae61-c93ea06da40a.png)


<b>This complexity was solved by cyclical get requests
to the url in Headers with changing the variable
value for loading all festivals:</b>
![image](https://user-images.githubusercontent.com/116018998/216822354-64f18df9-6eac-4819-94b1-22b45f2d829e.png)


<b>The next difficulty was that FAQs was
also loaded dynamically by scrolling down the page.
These are the requests the client sends when scrolling down.</b>
![image](https://user-images.githubusercontent.com/116018998/216822893-32061541-ce4a-4d0c-8484-1de987578643.png)


<b>This problem was solved without using Selenium
by getting requests to the address,
as "#faq" was added when the cursor was in the FAQs block:</b>
![image](https://user-images.githubusercontent.com/116018998/216823116-111d3103-c822-4177-9939-fcf445f01de2.png)


<b>But here we had to face another problem.
Each question was also loaded dynamically using JavaScript:</b>
![image](https://user-images.githubusercontent.com/116018998/216823279-3392e39d-80c4-4d01-85d1-ba1e86a4e074.png)

<b>Extracting textual information only
using Beautifulsoup and find methods
did not provide information in an ordered
form that could be used in the future.
Therefore, the information was converted
to json format with a collection of dictionaries
and lists, from which FAQs questions and
answers were extracted in a convenient and readable form.</b>

<b>As a result of completing the code, we get:</b>
<b>- JSON files for each festival with FAQs information</b> https://github.com/imartov/parser_festivals/tree/main/faqs_data_ever_fest
<b>- HTML file for each festival</b> https://github.com/imartov/parser_festivals/tree/main/ever_fest_html
<b>- most importantly - one JSON file for all festivals with ordered and required information</b> https://github.com/imartov/parser_festivals/blob/main/info_fests.json
