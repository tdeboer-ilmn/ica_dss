def find_item_by_name(method,name,**kwargs):
    '''Find any item with the provided name in the list of items for the method
    
    Parameters
      method: the method for the API call to use in the search
              Examples: vols_api.list_volumes, files_api.list_files, folders_api.list_folders
      name: String - The name that will be searched for (name attribute for the items)
    '''
    page_size = 1000
    l = []
    r = method(page_size=page_size, **kwargs)
    l.extend(r.items)
    #We may get more pages, if so, load them all
    # Page size max == 1000
    while r.next_page_token:
        r = method(page_size=page_size,page_token=r.next_page_token, **kwargs)
        l.extend(r.items)
    return next((item for item in l if item.name == name), False)

def list_all_items(method,**kwargs):
    '''List all items for the method. Will cycle through all pages that are available
    
    Parameters
      method: the method for the API call to use
              Examples: vols_api.list_volumes, files_api.list_files, folders_api.list_folders
    '''
    page_size = 1000
    l = []
    r = method(page_size=page_size, **kwargs)
    l.extend(r.items)
    #We may get more pages, if so, load them all
    # Page size max == 1000
    while r.next_page_token:
        r = method(page_size=page_size,page_token=r.next_page_token, **kwargs)
        l.extend(r.items)
    return l