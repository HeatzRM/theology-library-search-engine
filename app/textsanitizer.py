from .stopwordsremover import StopWordsRemover
from .stemmer import Stemmer

class TextSanitizer(object):
	def sanitize(self, text = None):
		text = Stemmer().stem(StopWordsRemover().remove(text))
		return text

