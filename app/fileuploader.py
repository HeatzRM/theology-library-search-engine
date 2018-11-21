class FileUploader(object):
	def pdf_uploader(self, request, destination, pdf_directory):
		''' uploads the pdf in the directory'''
		pdf_destination = ''
		pdf_file_name = ''
		try:
			for file in request.files.getlist("pdf"):
				filename = file.filename
				destination = "/".join([pdf_directory, filename])
				file.save(destination)
		except Exception as ex:
			print(ex)
			


	def pages_uploader(self, request, destination, page_directory):
		''' uploads the image pages in the directory'''
		try:
			for file in request.files.getlist("pages"):
				filename = file.filename
				destination = "/".join([page_directory, filename])
				file.save(destination)
		except Exception as ex:
			print(ex)

	def cover_uploader(self, request, destination, cover_image_directory):
		''' uploads the cover image in the directory'''
		try:
			for file in request.files.getlist("cover_img"):
				filename = file.filename
				destination = "/".join([cover_image_directory, filename])
				file.save(destination)
		except Exception as ex:
			print(ex)

