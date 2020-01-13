# SAGE_Shashank
MINDS MS Student competiton Web crawling

As per the competition, we need to find an automated way of getting the number of orbital
launches in the 'Orbital launches' table in Wikipedia Orbital Launches(https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches) if at least one of its payloads is reported as 'Successful', 'Operational', or 'En Route'.

In the script I've used lxml to build a tree and then using xpath navigated the page structure.
Using simple logic I've constructed a dataframe and for each launch whose payloads belong any one of the three
categories I've added the date inside the dataframe. In the end using group and count, dumped the output
to an output.csv.

