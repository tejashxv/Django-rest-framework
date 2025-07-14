from rest_framework.pagination import PageNumberPagination,CursorPagination
from django.core.paginator import EmptyPage
from rest_framework.exceptions import ValidationError


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
    
    
def paginate(data, paginator, pagenumber):
    if int(pagenumber) > paginator.num_pages:
        raise ValidationError({'error': 'Page number is out of range'})
    
    try:
        prev_page_no = paginator.page(int(pagenumber)).previous_page_number()
    except EmptyPage:
        prev_page_no = None
        
    try:
        next_page_no = paginator.page(int(pagenumber)).next_page_number()
    except EmptyPage:
        next_page_no = None
        
    data_to_show = paginator.page(int(pagenumber)).object_list
    
    return {
            "pagination": {
            "prev_page_no": prev_page_no,
            "next_page_no": next_page_no,
            "total_pages": paginator.num_pages,
            "current_page": int(pagenumber),
            "has_next": paginator.page(int(pagenumber)).has_next(),
            "has_previous": paginator.page(int(pagenumber)).has_previous(),
            "is_first": paginator.page(1).number == int(pagenumber),
            "is_last": paginator.page(paginator.num_pages).number == int(pagenumber),
        },
        "results": data_to_show,
    } 