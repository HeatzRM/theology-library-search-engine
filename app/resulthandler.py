#from .tfidfhandler import TFIDFHandler
from app.models import Article
from .search import SearchHandler
from .texthandler import TextHandler
from .tfidfhandler import TFIDFHandler
import os
import json

def query_database_by_book_id(book_list):
    #queries to the database by id, must be a list of string titles
    out_articles = []
    for book_id in book_list:
        out_articles.append(Article.query.filter_by(id=book_id).first())
    return out_articles

def get_search_result(query):
    '''
    Search method by TFIDF and if one of the 
    words exist in any of the documents

    Params: 
        query: String
    '''

    print("\n\nSearch Start - Searching by book attributes")
    query = query.lower()
    list_of_books = []
    APP_ROOT = os.path.dirname(os.path.abspath(__file__)) #get absolute directory

    #Get all books
    json_books = ''
    try:
        json_books = TextHandler().OpenTextFrom(APP_ROOT+"//static", "index.JSON")
        json_books = json.loads(json_books)
    except Exception as ex:
        print(ex)

    #Search based on the all the attributes except the text(content)
    list_of_books = SearchHandler().search_books(query, json_books)
    books = json_books
    
    #phrase search
    #Search based on content of the books
    TFIDF = TFIDFHandler()
    TFIDF.query = query
    #print('Query:' + TFIDF.query)
    books = TFIDF.calc_tfidf_per_book(books)
    books = TFIDF.sort_by_tf_idf(books)

    books = set(books)
    #print(str(list_of_books) + 'list of books')
    list_of_books = set(list_of_books)
    list_of_books = set.union(list_of_books, books)

    #print(str(list_of_books) + 'phrase search')

    #redo search 
    #Search books only if any of the query of the words exist
    if(len(list_of_books) == 0):
        print("\n\nStarting Split Query Search")
        query = query.split(' ')

        final_split_search_books = {}
        for q in query:
            print('\nSearching for ' + q)
            split_search_books = json_books 
            TFIDF = TFIDFHandler()
            TFIDF.query = q
            split_search_books = TFIDF.calc_total_tfidf_per_book(split_search_books)

            for book in final_split_search_books:
                print(final_split_search_books[book]['TFIDF'])

            for book in split_search_books:
                final_split_search_books.update({split_search_books[book]['ID']  : split_search_books[book]})
        
        final_split_search_books = TFIDF.sort_by_tf_idf(final_split_search_books)
        
        print(final_split_search_books)
                
        
        print("Split Search end\n\n")    
        return query_database_by_book_id(final_split_search_books)    

    print("Search end\n\n")      
    return query_database_by_book_id(list_of_books)

def make_list_cluster_docs():
    documents_list = []
    APP_ROOT = os.path.dirname(os.path.abspath(__file__)) #get absolute directory
    json_books = TextHandler().OpenTextFrom(APP_ROOT+"//static", "index.JSON")
    json_books = json.loads(json_books)
    for book_id in json_books:
        documents_list.append(json_books[book_id]['RemovedStopWordsText'])
    return documents_list

def get_specific_search(queries):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    json_books = ''
    try:
        json_books = TextHandler().OpenTextFrom(APP_ROOT+"//static", "index.JSON")
        json_books = json.loads(json_books)
    except Exception as ex:
        print(ex)
    return query_database_by_book_id(SearchHandler().specific_search(queries, json_books))
    
    

