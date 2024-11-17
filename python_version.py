from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton,QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap



import struct
import os


#....................................................crop_black_box............................................


def crop_black_box(pic, width, height):
    # Initialize variables to track the bounding box of non-black pixels
    min_x, max_x = width, 0
    min_y, max_y = height, 0

    # Find the bounding box of non-black pixels
    for y in range(height):
        for x in range(width):
            if pic[y][x * 3] != 0 or pic[y][x * 3 + 1] != 0 or pic[y][x * 3 + 2] != 0:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    # If no non-black pixels are found, return the original image
    if min_x > max_x or min_y > max_y:
        print("No non-black pixels found.")
        return pic, width, height

    # Calculate new width and height of the cropped image
    new_width = max_x - min_x + 1
    new_height = max_y - min_y + 1

    # Create a new image with the cropped dimensions
    new_pic = [[0] * (new_width * 3) for _ in range(new_height)]
    
    # Copy non-black pixels into the new image
    for y in range(new_height):
        for x in range(new_width):
            old_x = min_x + x
            old_y = min_y + y
            new_pic[y][x * 3] = pic[old_y][old_x * 3]      # Blue
            new_pic[y][x * 3 + 1] = pic[old_y][old_x * 3 + 1]  # Green
            new_pic[y][x * 3 + 2] = pic[old_y][old_x * 3 + 2]  # Red
    return new_pic,new_height,new_width





#....................................................Create_avg_color............................................

def avgcolor(mat):
    red, green, blue, n = 0, 0, 0, 0
    for i in range(len(mat)):  
        for j in range(len(mat[i])):
            if j % 3 == 0: 
                blue += mat[i][j]
            elif j % 3 == 1: 
                green += mat[i][j]
            elif j % 3 == 2: 
                red += mat[i][j]

            n += 1

    if n == 0:
        return 0, 0, 0
    
    return red // n, green // n, blue // n

#....................................................Mix_the_photo...............................................


    # i,j,m,n=0,0,0,0
    # while i < height:
    #     while j < width*3 :
    #         if(i+div-1 < height and j+div-1 < width*3):
    #             for x in range(i+div):
    #                 for y in range(j+div*3):
    #                     mat[m][n]=pic[x][y]
    #                     n+=1
    #                 if(n<div):
    #                     n=0
    #                     m+=1
    #             red,blue,green=avgcolor(mat ,div)
    #         elif(i+div-1 < height and j+div-1 > width*3):
    #             siv = div
    #             while j+siv-1 > width*3:
    #                 siv-1
    #             for x in range(i+div):
    #                 for y in range(j+siv*3):
    #                     mat[m][n]=pic[x][y]
    #                     n+=1
    #                 if(n<siv):
    #                     n=0
    #                     m+=1
    #             red,blue,green=avgcolor(mat ,div,siv)
    #         elif(i+div-1 > height and j+div-1 < width*3):
    #             siv = div
    #             while j+siv-1 > height:
    #                 siv-1
    #             for x in range(i+siv):
    #                 for y in range(j+div*3):
    #                     mat[m][n]=pic[x][y]
    #                     n+=1
    #                 if(n<siv):
    #                     n=0
    #                     m+=1
    #                 red,blue,green=avgcolor(mat ,siv,div)
    #         else:
    #             siv = div
    #             while j+siv-1 > height:
    #                 siv-1
    #             hi=siv
    #             siv = div
    #             while j+siv-1 > width*3:
    #                 siv-1
    #             for x in range(i+hi):
    #                 for y in range(j+siv*3):
    #                     mat[m][n]=pic[x][y]
    #                     n+=1
    #                 if(n<siv):
    #                     n=0 
    #                     m+=1
    #             red,blue,green=avgcolor(mat ,hi,siv)
    #         j+=div

    #     if(i+div-1 < height and j+div-1 > width*3):
    #         j=0
    #         i+=div


    #chat code   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(



def mix(pic,width,height,div):
    pic1=[[0]*(width*3)for _ in range(height)]

    i , ii = 0 , 0
    while i < height:
        j , jj = 0 , 0 
        while j < width * 3:
            m, n = 0, 0
            hi = min(div, height - i)
            siv = min(div, (width * 3 - j)// 3) 
            mat = [[0] * (div * 3) for _ in range(div)]
            for x in range(hi):
                for y in range(siv * 3):
                    mat[m][n] = pic[i + x][j + y]
                    n += 1
                    if n >= div * 3:
                        n = 0
                        m += 1
            
            red, green, blue = avgcolor(mat)
                
            pic1[ii][jj] = blue
            jj += 1
            pic1[ii][jj] = green
            jj += 1
            pic1[ii][jj] = red
            jj += 1
            
            j += div * 3
        i += div
        ii+=1
    pic1 , new_height , new_width = crop_black_box(pic1, len(pic1[0])//3, len(pic1))
    return pic1,new_height,new_width

#    :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(   :(
            



#..............................................class MyWindow....................................................
 

class MyWindow(QMainWindow):
    
#....................................................main_reading_part...........................................


    def img(self,new_height,new_width):
        path = self.page1.le1.text().strip()
        div = self.page1.le2.text()
        if not os.path.isfile(path):
            QMessageBox.critical(self, "Error", "The specified file does not exist!")
            return
        if(div.isdigit):
            try:
                div = int(self.page1.le2.text().strip())
                if div <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.critical(self, "Error", "Division value must be a positive integer!")
                return
        else :
            QApplication.critical(self,"Error","Error !")
        # Suppose we have a byte sequence: 0x01 0x00 0x02 0x00 0x0A 0x00 0x00 0x00
        # It represents two 16-bit (2-byte) unsigned integers and one 32-bit (4-byte) unsigned integer

        binary_data = b'\x01\x00\x02\x00\x0A\x00\x00\x00'

        # Use struct.unpack to extract the integers
        # 'H' represents 2-byte unsigned integers, 'I' represents a 4-byte unsigned integer
        values = struct.unpack('HHI', binary_data)

        print(values)  # Output: (1, 2, 10)


        # reading the photo ? : my idea is using reding as binary and read every character
        img_file = open(path,"rb") 
        low_img_file = open("img_file.bmp","wb")
        
        #read 14 bit file header and then read 40 bit info header
        file_header = img_file.read(14)
        file_info = img_file.read(40)
        low_img_file.write(file_header)
        

        print(file_header) # output: b'BM\x8a{\x0c\x00\x00\x00\x00\x00\x8a\x00'


        file_type = struct.unpack("H",file_header[0:2])[0]
        file_size = struct.unpack("I",file_header[2:6])[0]
        offset_data = struct.unpack("I",file_header[10:14])[0]


        print(file_info) # output: <_io.BufferedReader name='sample_640 426.bmp'>


        width = struct.unpack("I",file_info[4:8])[0]
        height = struct.unpack("I",file_info[8:12])[0]
        bit_count=struct.unpack("H",file_info[14:16])[0]
        
        # Update width and height
        new_width = width // div
        new_height = height // div
        print(f"New dimensions: {new_width}x{new_height}")

        # Write updated BITMAPINFOHEADER to the new file
        new_file_info = (
            file_info[0:4] +  # Keep size of the header
            struct.pack("I", new_width) +  # New width
            struct.pack("I", new_height) +  # New height
            file_info[12:40]  # Remaining unchanged header fields
        )
        
        low_img_file.write(new_file_info)
        # Ensure it's a valid BMP file

        if(file_type != 0x4D42):
            print("Error: Not a valid BMP file.")
            return


        # Ensure it is a 24-bit BMP file
        if bit_count != 24:
            print("Error: Only 24-bit BMP files are supported.")
            return

        print(f"file_size: {file_size}")
        print(f"file_type: {file_type}")
        print(f"file_offset: {offset_data}")
        print(f"Image dimensions: {width}x{height}")
        print(f"Bit depth: {bit_count}-bit")

        # Seek to the beginning of pixel data
        img_file.seek(offset_data)

        # Calculate row padding (each row must be aligned to a multiple of 4 bytes)
        row_padding = ( 4 - ( width * 3 ) % 4 ) % 4

        # pixel loop

        t=0
        print(f"The file is in part: {0}%")
        
        # table that have two dimention

        pic=[[0]*(width*3)for _ in range(height)]
        for y in range(height):
            row = img_file.read(width*3)
            for x in range(width):


                blue=row[x*3]
                green=row[x*3+1]
                red=row[x*3+2]
                
                
                # print(f"Pixel ({x},{y}) : Red : {red} Green : {green} Blue : {blue}")


                #filling the new image of file
                pic[y][x*3]=blue
                pic[y][x*3+1]=green
                pic[y][x*3+2]=red

            img_file.read(row_padding)
            
            #how much has been done 
            s = round((y*100)/height) 
            if s > t + 9 :
                t = s
                self.page1.progressBar.setValue(t)


        pic,new_height,new_width=mix(pic,width,height,div)




        #The file where are filling this is the last part
        for y in range(new_height):
            low_img_file.write(bytes(pic[y])+ b'\x00' * row_padding)



        remaining_data = img_file.read()
        low_img_file.write(remaining_data)

        #Closing folders


        low_img_file.close()
        img_file.close()
        

        

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Display Example")

        # Create a stacked widget to hold the two pages
        self.stacked_widget = QStackedWidget(self)

        # Load the first page (controls page)
        self.page1 = loadUi("IntGra.ui")
        self.stacked_widget.addWidget(self.page1)

        # Load the second page (image display page)
        self.page2 = loadUi("imgui.ui")
        self.stacked_widget.addWidget(self.page2)

        # Set the layout and show the stacked widget
        self.setCentralWidget(self.stacked_widget)

        # Buttons to switch between pages
        self.page1.br.clicked.connect(self.show_image_page)  # A button to show the image page
        self.page1.bre.clicked.connect(self.reset)          # A button to reset
        self.page1.bc.clicked.connect(self.close)           # A button to close the app
        self.page2.br_2.clicked.connect(self.openui)
    def show_image_page(self):
        # Load and display the image on page2
        new_height,new_width=0,0
        self.img(new_height,new_width)
        pixmap = QPixmap(r"C:\Users\kakois\Documents\Jad_project\lowering_img_resulution\img_file.bmp")  # Adjust the path if necessary
        if pixmap.isNull():
            print("Error loading image!")
        self.page2.imageLabel.setPixmap(pixmap)
        self.page2.imageLabel.setScaledContents(True)

        # Switch to the image page
        self.stacked_widget.setCurrentWidget(self.page2)

    def reset(self):
        # Reset the input fields
        self.page1.le1.setText("")
        self.page1.le2.setText("")
        self.page1.progressBar.setValue(0)

    def openui(self):
        self.stacked_widget.setCurrentWidget(self.page1)
# Initialize and run the app

app = QApplication([])
windows = MyWindow()
windows.show()
app.exec_()