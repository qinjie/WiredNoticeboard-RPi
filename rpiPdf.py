
import os
import utilsWand
import utilsOther
import shutil

####
# This script is the main script to download slideshow files from server
# 1. Get file list in play order into file_list.txt
# 2. Download files into "download" folders
# 3. For each file in file_list with index i
# 	Get file from download folder
# 	If it's a image file, copy to "pictures" folder and rename it as "<i>_<filename>"
# 	If it's a pdf file, export it as images to "pictures" foder with name "<i>_<filename>_<page>"
# 4. Run Feh with slide show
# 5. Play video files
####

FOLDER_DOWNLOAD = "Data\Pdf"
FOLDER_IMAGES = "Data\Image"
fOLDER_VIDEO = "Data\Video"

# Get file_list.txt
# Exit if file_list.txt is the same, else proceed with following
#TODO


# Download files into download folder
# Clean up download folder before downloading
#TODO

def pdfFile() :
# Read from file_list.txt
    file_list = []
    with open("file_list.txt") as f:
        for line in f:
            file_list.append(line.strip())

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(cur_dir, FOLDER_IMAGES)

    # Clear output folder
    if os.path.exists(output_path):
        print "Clean up output folder..."
        flist = os.listdir(output_path)
        for f in flist:
            os.remove(os.path.join(output_path,f))

    # Process input files into output folder
    #   copy image and export pdf
    for index, file_name in enumerate(file_list):
        new_file_name = "{0:04}_{1}".format(index, file_name)
        print new_file_name
        # Export PDF into images
        input_file = os.path.join(cur_dir, FOLDER_DOWNLOAD, file_name)

        if input_file.endswith('.pdf'):
            # Export PDF to images
            input_file2 = os.path.join(cur_dir, FOLDER_DOWNLOAD, new_file_name)
            shutil.copy2(input_file, input_file2)
            utilsWand.pdf_to_png(input_file2, output_path)
            os.remove(input_file2)
        elif utilsOther.get_image_type(input_file):
            # Copy image to output folder
            output_file = os.path.join(output_path, new_file_name)
            shutil.copy2(input_file, output_file)

if __name__ == '__main__' :
    pdfFile()

