# fusion360csvexport
Export one stl file each row of a csv file containing a list of parameters values.
This allows you to generate many variants of the same parametric design in one go !

## CSV structure
*Note: an example csv file is located in /example folder to illustrate the folowing instructions.*

### Delimiter
Use the comma `,` to separate values

### First row
Parameter names, same as in your fusion parameters windows (see below)

![Fusion360 parameters window location](/doc/parameters%20in%20fusion360.png)

### Other rows
Parameter values

### First column
The column except a mandatory `fileName` parameter which values are used to name each output file.

*Note: the **.stl** extension is added automatically*

This has been done to give you a more flexible way to name you files.
This allows you to use a simple formula from your spreadsheet application as seen below:

![Example of an automated name generation formula](/doc/naming%20is%20easy.png)

## Usage
Clone or download & uncompress this repository somewhere on your disk.

*Note: it doesn't have to be located in the standard fusion360 scripts folder*

Add the script to your list of custom scripts as showed below:

![Scripts and Add-Ins menu Location](/doc/fusion360%20scripts%20menu.png)
![Adding a new script](/doc/fusion360%20add%20custom%20script.png)

Select the script and run it, and follow the steps:

![Adding a new script](/doc/fusion360%20run%20script.png)