from django.db import models
from django.core.exceptions import ValidationError
import re

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Niche(models.Model):
      name = models.CharField(max_length=200, unique=True)
      

      def __str__(self):
            return self.name


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    domain = models.URLField(unique=True)
    slug = models.SlugField(unique=True)
    niche = models.ForeignKey(Niche, on_delete=models.CASCADE)
    domain_data_json = models.JSONField(blank=True, null=True)
    domain_pages_data_json = models.JSONField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_lead = models.BooleanField(default=False)
    traffic_us = models.IntegerField(blank=True, null=True)
    pages_in_serps = models.IntegerField(blank=True, null=True)
    pitch_video = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): 
                if not self.slug:
                        self.slug = slugify(self.name) 
                return super().save(*args, **kwargs)
        
    def get_absolute_url(self):
                return reverse('company-detail', kwargs={'company_slug': self.slug})
    
    def get_admin_url(self):
        return reverse("admin:lf_company_change", args=(self.id,))
    
    @property
    def pitch_youtube_id(self):
        if 'youtube' in self.pitch_video:
            match = re.search('(?<=v=)[^&]+', self.pitch_video)
            video_id = match.group() if match else None
            return video_id


class Page(models.Model):
	url = models.URLField(unique=True)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	textrazor_json = models.JSONField(blank=True, null=True)

	def __str__(self):
        	return self.url


class SEOdomain(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    total_pages = models.IntegerField(null=True, blank=True)
    total_keywords = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)


class TopicalMap(models.Model):
    niche = models.ForeignKey(Niche, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.niche is None and self.company is None:
            raise ValidationError("Error: Both Niche & Company cannot be None!")
      
        super(Entity,self).save(*args,**kwargs)


class Entity(models.Model):
    topical_map = models.ForeignKey(TopicalMap, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    connection = models.ManyToManyField('self')
    textrazor_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class MarketingCategory(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
          return self.name


class PortfolioItem(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    link = models.URLField(blank=True, null=True)
    client = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    is_ghostwritten = models.BooleanField(default=False)
    category = models.ForeignKey(
        MarketingCategory, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
    
    @property
    def youtube_id(self):
        if 'youtube' in self.link:
            match = re.search('(?<=v=)[^&]+', self.link)
            video_id = match.group() if match else None
            return video_id
    
    def save(self, *args, **kwargs): 
            if not self.slug:
                    self.slug = slugify(self.title) 
            return super().save(*args, **kwargs)
    

class CodeProject(models.Model):
    title = models.CharField(max_length=200)
    live_url = models.URLField(blank=True, null=True)
    screenshot_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self): return self.title