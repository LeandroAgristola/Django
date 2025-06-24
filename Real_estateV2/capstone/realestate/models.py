from django.db import models
import os

# Model representing a development project
class development(models.Model):
    # Title of the development, limited to 50 characters
    title = models.CharField(max_length=50)
    
    # Short description or content about the development, limited to 200 characters
    content = models.CharField(max_length=200)
    
    # Image associated with the development, stored in the 'developments' directory
    image = models.ImageField(upload_to='developments')
    
    # Brochure or PDF file associated with the development, stored in 'developments_pdfs/' directory
    brochurePaper = models.FileField(upload_to='developments_pdfs/')
    
    # Timestamp for when the development was created, automatically set on creation
    created = models.DateTimeField(auto_now_add=True)
    
    # Timestamp for when the development was last updated, automatically set on save
    updated = models.DateTimeField(auto_now=True)

    # Meta options for the model
    class Meta:
        # Singular name for the model in the admin interface
        verbose_name = 'development'
        
        # Plural name for the model in the admin interface
        verbose_name_plural = 'developments'

    # String representation of the model, showing the title
    def __str__(self):
        return self.title
    
    # Custom delete method to remove associated files from the filesystem
    def delete(self, *args, **kwargs):
        # If an image exists, remove it from the filesystem
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        
        # If a brochure or PDF file exists, remove it from the filesystem
        if self.brochurePaper:
            if os.path.isfile(self.brochurePaper.path):
                os.remove(self.brochurePaper.path)
        
        # Call the parent class's delete method to remove the model instance from the database
        super().delete(*args, **kwargs)
