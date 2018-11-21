from .coveruploader import cover_inserter
from .textrecognition import convert_list_img_to_txt
from .pdfconverter import convert_pdf_to_text
from .converted_text_updater import converted_text_update

class UploadHandler(object):

	#region input_article
    @property
    def input_article(self):
        return self._input_article

    @input_article.setter
    def input_article(self, value):
        self._input_article = value

    @input_article.deleter
    def input_article(self):
        del self._input_article
    #endregion

    #region cover_image_destination
    @property
    def cover_image_destination(self):
        return self._cover_image_destination

    @cover_image_destination.setter
    def cover_image_destination(self, value):
        self._cover_image_destination = value

    @cover_image_destination.deleter
    def cover_image_destination(self):
        del self._cover_image_destination
    #endregion

    #region cover_image_name
    @property
    def cover_image_name(self):
        return self._cover_image_name

    @cover_image_name.setter
    def cover_image_name(self, value):
        self._cover_image_name = value

    @cover_image_name.deleter
    def cover_image_name(self):
        del self._cover_image_name
    #endregion

    #region list_of_page_image_names
    @property
    def list_of_page_image_names(self):
        return self._list_of_page_image_names

    @list_of_page_image_names.setter
    def list_of_page_image_names(self, value):
        self._list_of_page_image_names = value

    @list_of_page_image_names.deleter
    def list_of_page_image_names(self):
        del self._list_of_page_image_names
    #endregion

    #region list_of_image_directory
    @property
    def list_of_image_directory(self):
        return self._list_of_image_directory

    @list_of_image_directory.setter
    def list_of_image_directory(self, value):
        self._list_of_image_directory = value

    @list_of_image_directory.deleter
    def list_of_image_directory(self):
        del self._list_of_image_directory
    #endregion
    
    #region pdf_destination
    @property
    def pdf_destination(self):
        return self._pdf_destination

    @pdf_destination.setter
    def pdf_destination(self, value):
        self._pdf_destination = value

    @pdf_destination.deleter
    def pdf_destination(self):
        del self._pdf_destination
    #endregion

    #region pdf_name
    @property
    def pdf_name(self):
        return self._pdf_name

    @pdf_name.setter
    def pdf_name(self, value):
        self._pdf_name = value

    @pdf_name.deleter
    def pdf_name(self):
        del self._pdf_name
    #endregion

    def run_converters(self):
        print("----------------------------")
        print("STARTING DATABASE INSERT")
        try:
            print("STARTING COVER IMAGE INSERT: ")
            cover_inserter(self._cover_image_destination, self._cover_image_name, self._input_article)
            print('COVER IMAGE INSERT COMPLETED!')
        except Exception as ex:
            print('Error Occurred in Cover Image Insert' + str(ex))
        
        try:
            print("STARTING IMAGE PAGES CONVERSION")
            convert_list_img_to_txt(self._list_of_image_directory, self._list_of_page_image_names, self._input_article)
            print("IMAGE PAGES CONVERSION TO TEXT COMPLETED!")
        except Exception as ex:
            print(ex)
            print('Error Occured in Page Conversion: ' + str(ex) )

        try:
            print("STARTING PDF CONVERSION: ")
            convert_pdf_to_text(self._pdf_destination, self._pdf_name, self._input_article)
            print("PDF CONVERSION TO TEXT COMPLETED!")
        except Exception as ex:
            print('Error Occurred in PDF Conversion: ' +  str(ex))

        try:
            print("STARTING INSERTING ALL IMAGES PAGE TEXT AND PDF TEXT INTO index.JSON")
            converted_text_update(self._input_article)
        except Exception as ex:
            print('Error Occurred in Converted Text Update: ' +str( ex))
        print("FINISHED DATABASE INSERT FOR " + str(self._input_article.id))
        print("----------------------------")

