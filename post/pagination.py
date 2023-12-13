class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

def set_pagination(self,data,serializer):
    page = self.paginate_queryset(data)
    if page is not None:
        serializer = self.get_paginated_response(serializer(page, many=True).data)
    else:
        serializer = serializer(data, many=True)
    return serializer