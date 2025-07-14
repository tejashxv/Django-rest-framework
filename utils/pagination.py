from rest_framework.pagination import PageNumberPagination,CursorPagination



class LargeResultPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_query_param = 'page_size'
    
class SmallResultPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'page_size'
    
class CustomCursorPagination(CursorPagination):
    page_size = 2
    ordering = 'id'