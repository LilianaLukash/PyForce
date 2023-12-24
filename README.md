# PyForce

A PyForce personal assistant that helps you not to forget to congratulate your contacts.

## Installation

Instructions for installing the project:
- Step 1: use command: <pip install .> from the directory setup.py of PyForce is located in
- Check Installed Packages: You can use pip list or pip show PyForce
-to Uninstall use pip uninstall PyForce


## Usage

To use the assistant you need to enter your contacts' names, phones, birthday dates, and, if you want, an email and notes.
How to use?
-First add a contact. To add a contact you need to type in a name and a phone. Once you did it you have conact saved. However, the assistant won't be able to provide
you a list of birthdays without a birthday date. You should provide a birthday date either. Once you did it, if you want to see upcoming birthdays, you simpl need
to type in command <birthdays>. The assistant will provide you with a list of upcoming birthdays for 7 days. The assistant also is able to give you list for 
<parametr> days forward. Simply type in <birtdays <parametr>>. For example birthdays 14, and it will give you a list of birthdays for upcoming 14 days. 

Full list of commands is next:

"'add-contact then <enter>. Successively type in <name><phone><birthday><address><email>'\n"
"'add-phone <name> <phone>'to add a phone to the existing contact"
"'add-email <name> <email>' to add an e-mail to the existing contact"
"'add-email <name> <phone> <email>' to add an e-mail to the existing contact"
"'add-address <name> <actual-adвress-in-one-string>' to add an address the existing contact"
"'add-note <name> <phone> <note>' to add note you must"
"'change-phone <name> <old phone> <new phone>' to change phone"
"'findall <criteria> search of contacts by criteria from 3 symbols"
"'phone <name>' to see a phone and a name input"
"'show-birthday <name>' to see birthday date for the contact"
"'change-birthday <name> <DD.MM.YYYY>'"
"'birthdays' to see upcoming birthdays for the next 7 days"
"'birthdays <number of days>'-> if you want to specify for how many days forward you want a list of birthdays"
"'all' to see all the addressbook"
"'delete' <name>  to delete the contact"
"'notes-help' if you want to see intstructions on how to add notes"
"'close' to end the assistant"


To use notes, use the following commands and instructions:

 If you want to add notes follow the instructions below: "
"'<noteadd : title : note >' - to add a note"
"'type in <tag, tag, tag>' if you want tags"
"'<notesall>' - to print all notes"
"'<notesfind : title>' - search a note by title"
"'<notesedit : title>' - search by title and re-write"
"'<findbytag : title>' - find a note by tag"
"'<addtag:title :<tag>>' add tag to a note by title"
"'<notesremove: title>' - remove a note by title"

## Configuration

Installation
To install PyForce, you can use pip:
pip install PyForce

Usage
After installation, you can import PyForce in your Python scripts:
import PyForce


## Contributing

Guidelines for contributing:
https://github.com/LilianaLukash/PyForce/

###Requirements
python =>=3.8





##License


MIT License

Copyright (c) [2023] [PyForce]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

