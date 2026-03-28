import logging
from django.utils import timezone
from .models import Keyword, ContentItem, Flag

logger = logging.getLogger(__name__)

def calculate_score(keyword_name, content_item):
    """
    Exact keyword match in title → score = 100
    Partial keyword match in title → score = 70
    Match in body → score = 40
    Case insensitive matching
    """
    keyword_name_lower = keyword_name.lower()
    title_lower = content_item.title.lower()
    body_lower = content_item.body.lower()

    if keyword_name_lower == title_lower:
        return 100
    if keyword_name_lower in title_lower:
        return 70
    if keyword_name_lower in body_lower:
        return 40
    
    return 0

def should_process_item_keyword(keyword, content_item):
    """
    Handle suppression logic:
    If a flag exists and is marked "irrelevant", it should NOT be recreated
    UNLESS ContentItem.last_updated is newer than the last_reviewed_at
    """
    try:
        existing_flag = Flag.objects.get(keyword=keyword, content_item=content_item)
        
        if existing_flag.status == 'irrelevant':
            # Re-evaluate only if content updated after last review
            if existing_flag.last_reviewed_at and content_item.last_updated > existing_flag.last_reviewed_at:
                return True
            return False # Suppressed
        
        return True # Process pending/relevant or if no review date set (though review usually sets date)
    except Flag.DoesNotExist:
        return True # New flag

def scan_content():
    keywords = Keyword.objects.all()
    content_items = ContentItem.objects.all()
    flags_created = 0
    flags_updated = 0

    for item in content_items:
        for kw in keywords:
            if not should_process_item_keyword(kw, item):
                continue
            
            score = calculate_score(kw.name, item)
            if score > 0:
                flag, created = Flag.objects.update_or_create(
                    keyword=kw,
                    content_item=item,
                    defaults={'score': score}
                )
                
                # If it was irrelevant but we are re-processing it because of update:
                # Reset status to pending so it gets reviewed again
                if flag.status == 'irrelevant' and flag.last_reviewed_at and item.last_updated > flag.last_reviewed_at:
                    flag.status = 'pending'
                    flag.save()

                if created:
                    flags_created += 1
                else:
                    flags_updated += 1
    
    logger.info(f"Scan complete. Created: {flags_created}, Updated: {flags_updated}")
    return flags_created, flags_updated
