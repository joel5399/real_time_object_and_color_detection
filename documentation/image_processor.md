# Image Processor
The image processor class is responsible for processing the image, analyzing it and looking for shapes with the respective color.

## image loading and preprocessing
The class does not require any initial input. However, in order to execute any of its methods, you must first load an image. During the image loading process, it will automatically undergo preprocessing and be saved as a binary image, facilitating the identification of shapes through contour detection. The constants used in the GaussianBlur method, as well as the threshold method, are experimental values that may need to be adjusted for different image qualities.

## search for patterns
After loading the image, you can use the searchForPatterns method to search for different shapes within the image. The discovered contours are stored in the contours attribute as a list of points, which are then utilized by the createPatterns method to create a class for each identified [pattern](/documentation/patterns.md). 
First, the createPatterns method verifies whether the contours form a polygon. Subsequently, the identified polygon is also examined to ensure it is of sufficient size and not convex in shape; if these conditions are not met, the contour is skipped. Afterward, the method proceeds to detect the center of the shape and determine its color, subsequently creating instances of the pattern classes.
To eliminate patterns that have been counted twice, the handlingDuplicateShapes function deletes patterns with similar centers. The current tolerance is set to 3%, but it can be adjusted if necessary.

## display the proceed Image
Using the displayProceedImg method, you can showcase the identified shapes on the original image. Additionally, it visualizes the center of each shape, and in the console, you will find the properties of the patterns displayed.