import os

class FolderGenerator(object):
	def create_upload_directory(self, target):
		''' Create Upload Directory'''
		if not os.path.isdir(target):
			os.mkdir(target)
		else:
			print("Could not create upload directory: {}".format(target))

	def create_page_directory(self, target):
		''' Create Page Directory'''
		page_directory = target + "/pages/"
		if not os.path.isdir(page_directory):
			os.mkdir(page_directory)
			return page_directory
		else:
			print("Could not create page  directory: {}".format(page_directory))

	def create_cover_directory(self, target):
		''' Create Cover Image Directory '''
		cover_image_directory = target + "/coverimage/"
		if not os.path.isdir(cover_image_directory):
			os.mkdir(cover_image_directory)
			return cover_image_directory
		else:
			print("Could not create cover image directory: {}".format(cover_image_directory))

	def create_pdf_directory(self, target):
		# Create PDF Directory
		pdf_directory = target + "/pdfs/"
		if not os.path.isdir(pdf_directory):
			os.mkdir(pdf_directory)
			return pdf_directory
		else:
			print("Could not create pdf image directory: {}".format(pdf_directory))