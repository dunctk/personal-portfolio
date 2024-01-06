from django.contrib import admin
import lf.models


@admin.register(lf.models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ('is_published', 'niche')

@admin.register(lf.models.Page)
class PageAdmin(admin.ModelAdmin):
    list_filter = ('company',)

admin.site.register(lf.models.Niche)

admin.site.register(lf.models.PortfolioItem)

admin.site.register(lf.models.MarketingCategory)

admin.site.register(lf.models.CodeProject)