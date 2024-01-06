from django.shortcuts import render
from django.http import Http404
from .models import (
	Company, Niche, Page, PortfolioItem, MarketingCategory,
	CodeProject
)

def index(request):
    examples_count = 0
    return render(request, 'index.html', {'examples_count': examples_count})


def about(request):
    return render(request, 'about.html')


def ladderfunnel_index(request):
	return render(request, 'ladder-funnel/ladderfunnel_index.html')


def lf_examples(request):
    examples_count = 0
    return render(request, 'examples/examples_list.html', {'examples_count': examples_count})


def lf_define(request):
    return render(request, 'lf-define.html')


def seo_index(request):
	companies = Company.objects.filter(is_published=True)
	niches = Niche.objects.all()
	niches_with_companies = [
		{
			'niche': niche,
			'companies': Company.objects.filter(niche=niche, is_published=True)
		} 
		for niche in Niche.objects.all()
	]
	return render(request, 'seo/seo_index.html', {
		'companies': companies, 'niches': niches, 'niches_with_companies': niches_with_companies
	})


def code_index(request):
	projects = CodeProject.objects.all()
	context = {'projects' : projects}
	return render(request, 'code/code_index.html', context=context)


def company_detail(request, company_slug):
	try:
		company = Company.objects.get(slug=company_slug)
		competitors = Company.objects.filter(
			niche=company.niche, 
			is_published=True
		).order_by('-traffic_us')
		homepage_entities = Page.objects.filter(
			company = company
		).first()
	except Company.DoesNotExist:
		raise Http404('Company does not exist')

	
	return render(request, 'seo/company_detail.html', {
		'company': company, 'competitors': competitors,
		'homepage_entities': homepage_entities
	})


def company_detail_pitch(request, company_slug):
	try:
		company = Company.objects.get(slug=company_slug)
		competitors = Company.objects.filter(
			niche=company.niche, 
			is_published=True
		).order_by('-traffic_us')
		homepage_entities = Page.objects.filter(
			company = company
		).first()
	except Company.DoesNotExist:
		raise Http404('Company does not exist')

	
	return render(request, 'seo/company_detail_pitch.html', {
		'company': company, 'competitors': competitors,
		'homepage_entities': homepage_entities
	})


def case_studies(request):
	return render(request, 'seo/case_studies.html')


def content_writing(request):
	portfolio_items = PortfolioItem.objects.filter(category_id=1)
	return render(request, 'services/content_writing.html', {
		'portfolio_items': portfolio_items,
	})


def portfolio_index(request):
	portfolio_items = PortfolioItem.objects.all()
	categories = MarketingCategory.objects.all()
	return render(request, 'portfolio/portfolio_index.html', {
		'portfolio_items': portfolio_items,
		'categories': categories,
	})

def portfolio_video(request):
	portfolio_items = PortfolioItem.objects.filter(category_id=2)
	return render(request, 'portfolio/portfolio_video.html', {
		'portfolio_items': portfolio_items,
	})