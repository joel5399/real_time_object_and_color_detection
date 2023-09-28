# Real time object and color detection

As part of the [FHGR BSc Mobile Robotics](https://fhgr.ch/mr) an application to detect patterns and their color has been developed
as a group project by [Joshua Stutz](https://github.com/FidibusHex45) and  [Joel Flepp](https://github.com/joel5399) in the 5th
semester. The Project definition is stored [here](./requirements/Software_Engineering_Project_Definition_V1.pdf).

## structure documentation
This README provides a concise overview of the entire project. Further details and information can be accessed through the provided links.

## Software architecture
The structure of the software can be found [here](./documentation/software_architecture.md)

## Read images
The images will be captured using a webcam connected via USB to the laptop where the application will run. For testing purposes you can also run the application with a static image. More information can be found [here](./documentation/read_images.md).

## Main function
As previously mentioned, the primary function of the application is to edit images, search for patterns, and detect their colors. Detailed information about the implementation can be found [here](./documentation/image_processor.md).

## Logging
Another requirement is that all the founded patterns are logged into a csv. How this is implemented can be found [here](./documentation/logging.md).

## Visualisation
To show whitch patterns are found, a small window will appear and show the founded patterns to the user. Further information are stored [here](./documentation/visualisation.md).


