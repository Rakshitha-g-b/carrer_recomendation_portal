# recommender/models.py
from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"
    
    class Meta:
        unique_together = ('name', 'state') # A city name should be unique within a state
        verbose_name_plural = "Cities"


# Define choices for streams that colleges might offer
# These should ideally align with your STREAM_INFO keys for consistency
COLLEGE_STREAM_CHOICES = [
    ('Science', 'Science'),
    ('Commerce', 'Commerce'),
    ('Arts/Humanities', 'Arts/Humanities'),
    ('Vocational', 'Vocational/Diploma'), # Added for more college types
    ('Other', 'Other'),
]

class College(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # To represent what broad streams this college is known for
    # A college can offer multiple streams
    offered_streams = models.ManyToManyField('StreamTag', blank=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"

class StreamTag(models.Model):
    name = models.CharField(max_length=50, choices=COLLEGE_STREAM_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display() # To show the readable name

# Optional: If you want to list specific courses within colleges
# class Course(models.Model):
#     college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
#     name = models.CharField(max_length=200) # e.g., "B.Sc. Physics", "B.Com (Hons)"
#     stream_tag = models.ForeignKey(StreamTag, on_delete=models.SET_NULL, null=True, blank=True)
#     duration_years = models.PositiveSmallIntegerField(null=True, blank=True)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} at {self.college.name}"