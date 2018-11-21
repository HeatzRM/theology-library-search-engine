
class DirectoryGetter(object):
	def get_page_image_directory(self, list_of_image_names, directory, target):
		#Create a list of image directories for the image converter
		#change os directoryos.chdir(os.path.dirname(__file__))
		list_of_image_directory = []
		for image in list_of_image_names:
			directory = str(target+"/pages/"+image)
			list_of_image_directory.append(directory)
		return list_of_image_directory

	def get_cover_image_directory(self, list_of_cover_image_names, directory, target):
		#Create a list of image directories for the image converter
		list_of_image_directory = []
		#change os directoryos.chdir(os.path.dirname(__file__))
		for image in list_of_cover_image_names:
			directory = str(target+"/cover/"+image)
			list_of_image_directory.append(directory)
		return list_of_image_directory

	def get_pdf_directory(self, list_of_pdf_names, directory, target):
		#Create a list of image directories for the image converter
		list_of_pdf_directory = []
		print()
		#change os directoryos.chdir(os.path.dirname(__file__))
		for image in list_of_pdf_names:
			directory = str(target+"/pdfs/"+image)
			list_of_pdf_directory.append(directory)
		return list_of_pdf_directory	