from django.urls import path, include, re_path
from django_distill import distill_path
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from lf.views import index, ladderfunnel_index, lf_define, about, lf_examples, seo_index, case_studies
from lf.views import company_detail, company_detail_pitch, code_index, content_writing, portfolio_index
from lf.views import portfolio_video
from lf.models import Company, PortfolioItem


def get_all_companies():
	for company in Company.objects.filter(is_published=True):
		yield {'company_slug': company.slug}


def get_all_leads():
	for company in Company.objects.filter(is_published=True, is_lead=True):
		yield {'company_slug': company.slug}

urlpatterns = [
	distill_path(
		"robots.txt",
		TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
		name='robots-txt',
	),
    	distill_path('', index, name='home'),
	distill_path('about/', about, name='about'),
	distill_path('ladder-funnel/', ladderfunnel_index, name='ladderfunnel-index'),
	distill_path('ladder-funnel/examples/', lf_examples, name='lf-examples'),
	distill_path('ladder-funnel/what-is-a-ladder-funnel/', lf_define, name='lf-define'),
	distill_path(
		'seo/example/<str:company_slug>/', company_detail, name='company-detail',
		distill_func=get_all_companies
	),
	distill_path(
		'seo/pitch/<str:company_slug>/', company_detail_pitch, name='company-detail-pitch',
		distill_func=get_all_leads
	),
	distill_path('seo/', seo_index, name='seo-index'),
	distill_path('services/content-writing/', content_writing, name='content-writing'),
	distill_path('seo/case-studies/', case_studies, name='seo-case-studies'),
	distill_path('code/', code_index, name='code-index'),
	distill_path('portfolio/content-marketing/', portfolio_index, name='portfolio-index'),
	distill_path('portfolio/video/', portfolio_video, name='portfolio-video')
]