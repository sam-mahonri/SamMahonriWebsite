from datetime import datetime, timedelta
from flask_babel import lazy_gettext as _

def format_relative_time(post_date, exact=False):
    now = datetime.now()  # Obtenha a hora e data atual na localização atual
    delta = now - post_date

    if not exact:
        if delta < timedelta(minutes=1):
            seconds = delta.seconds
            if seconds == 0:
                return _('Agora mesmo')
            else:
                return _('Agora mesmo - %(seconds)s segundos', seconds=seconds)
        elif delta < timedelta(hours=1):
            minutes = delta.seconds // 60
            if minutes == 1:
                return _('Há 1 minuto')
            else:
                return _('Há %(minutes)s minutos', minutes=minutes)
        elif delta < timedelta(days=1):
            hours = delta.seconds // 3600
            if hours == 1:
                return _('Há 1 hora')
            else:
                return _('Há %(hours)s horas', hours=hours)
        elif delta < timedelta(weeks=1):
            days = delta.days
            if days == 1:
                return _('Há 1 dia')
            else:
                return _('Há %(days)s dias', days=days)
        elif delta < timedelta(days=365):
            weeks = delta.days // 7
            if weeks == 1:
                return _('Há 1 semana')
            else:
                return _('Há %(weeks)s semanas', weeks=weeks)
        else:
            years = delta.days // 365
            if years == 1:
                return _('Há 1 ano')
            else:
                return _('Há %(years)s anos', years=years)
    else:
        return _('Em %(post_date)s', post_date=post_date.strftime("%d/%m/%Y %H:%M:%S"))
