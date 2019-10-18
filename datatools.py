class DataFile:

    def __init__(self, file_name):
        self.file_name = file_name
      
    """
    Writes data about pixels into a new text file.
    
    Each frame is given an ID, and is given a pixel count for its 
    heading. Under each frame, a list of the counted pixels appears with
    information about locations and colors (if this information is 
    provided)
 
    """
    def save_count_to_file(self, frame_count, pixel_count, pixels = None, locations = None):
        
        full_pixel_list = list()
        
        for i in range(0,len(locations)):
            x = locations[i][0]
            y = locations[i][1]
            r = pixels[i][0]
            g = pixels[i][1]
            b = pixels[i][2]
            
            current_pixel = Pixel(x,y,r,g,b)
            
            full_pixel_list.append(current_pixel)
            
        
        with open(self.file_name, "a") as count_file:
            count_file.write("frame: {:3} pixel count: {}\n".format(frame_count, pixel_count))
        
        if(pixels != None and locations != None):
            with open(self.file_name, "a") as count_file:
                for pixel in full_pixel_list:
                    count_file.write("\t{}\n".format(pixel.str()))
          

"""
The location and color of a single pixel.
"""     
class Pixel:
    
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g 
        self.b = b
        
    def str(self):
        return "Location: ({:3},{:3})\tRGB: ({:3},{:3},{:3})".format(self.x,self.y,self.r,self.g,self.b)
        
"""
given an observation and a function which takes a pixel and returns a 
boolean, prints the following info to a text file for each frame:
    The count of matching pixels
    a list of each matching pixel, its location, and its RGB value
"""     
def countPixels(observation, pixel_testing_function):
        pixel_count = 0;
        pixels = list()
        pixel_locations = list()
        for y in range(0, len(observation)):
            row = observation[y]
            for x in range(0, len(row)):
                pixel = row[x]
                if pixel_testing_function(pixel):
                    pixel_count += 1
                    pixels.append(pixel)
                    pixel_locations.append((x,y))
        
        return pixel_count, pixels, pixel_locations