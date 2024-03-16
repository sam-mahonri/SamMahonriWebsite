from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from .models.user import User
from .models.statistics import Statistics
from .models.general import GeneralSettings
from .models.image import Gallery
from .models.modalities import Modalities