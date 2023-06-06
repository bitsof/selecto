def get_page_title(*args):
    page_title = 'Selecto'
    if len(args) == 0:
        return page_title
    try:
        match args[0]:
            case 'index':
                page_title += ' - Index'
            
            case 'details':
                page_title += ' - ' + args[1]

            case 'review_list':
                page_title += ' - ' + args[1] + ' - Reviews'

            case 'review_details':
                page_title += ' - ' + args[1] + ' - Review'
            
            case 'contact_us':
                page_title += ' - Contact Us'
            
            case 'about_us':
                page_title += ' - About Us'
            
            case 'login':
                page_title += ' - Log In'
            
            case 'signup':
                page_title += ' - Sign Up'

        return page_title
    
    except (TypeError, IndexError) as e:
        return page_title