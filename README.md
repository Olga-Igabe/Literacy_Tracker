# Community Device & Digital Literacy Tracker

A Python command-line application that helps community coordinators manage
digital skills training and shared device lending. Built as part of our
trimester project bridging technology-driven youth entrepreneurship, digital
access, and community social welfare.

The tool allows coordinators to register community members of all ages
(children, youth, and adults, with guardian information recorded for
minors), log training workshops led by hired trainers or NGO partners,
track each member's progress on a given skill (Not Started, In Progress,
or Completed), manage a device inventory, handle lending and returns, and
generate simple reports. The system does not create or deliver course
content itself — its purpose is to give coordinators clear visibility into
who is being reached, how far along they are, and where devices currently
are.

## Tech stack

- Python 3
- MySQL (via `mysql-connector-python`)
- No GUI — terminal-based menu interface

## Project structure
literacy_tracker/
├── database.py       # connection + setup
├── schema.sql        # table definitions
├── main.py           # menu loop
├── members.py        # register member, update progress
├── workshops.py       # log workshop, attendance
├── devices.py        # add device, lend/return
├── reports.py        # view reports
├── .gitignore
└── .env               # DB credentials (not committed)