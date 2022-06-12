from django.db import models


#this class has just six values (Amber, Hazel, blue, green, brown and dark brown)
#to ensure the usage of the correct names, we can have constants
#to automaticaly insert the colors in database, we need to create a fixtures file (see fixtures folder)
#and create a migrate script (see migration folder)
class EyeColor(models.Model):
    AMBER = "Amber"
    HAZEL = "Hazel"
    BLUE = "Blue"
    GREEN = "Green"
    BROWN = "Brown"
    DARK_BROWN = "Dark Brown"

    color_name = models.CharField(max_length=50)
    #useful for printing tests
    def __str__(self) -> str:
        return f"Eye color: {self.color_name}"

    def __repr__(self) -> str:
        return str(self)