from django.template import Library  

register = Library()


@register.filter
def get_files(db, user_id):
	return db.filter(user__id=user_id)