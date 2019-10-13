class DataFile:

    def __init__(self, file_name):
        self.file_name = file_name
        
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
          
          
class Pixel:
    
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g 
        self.b = b
        
    def str(self):
        return "Location: ({:3},{:3})\tRGB: ({:3},{:3},{:3})".format(self.x,self.y,self.r,self.g,self.b)