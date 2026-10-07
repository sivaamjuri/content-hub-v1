from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.blocks import RichTextBlock, StructBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField


@register_snippet
class Category(models.Model):
    """
    Reusable Snippet — content editors manage categories from Wagtail admin.
    Linked to ArticlePage via ForeignKey.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class ArticlePage(Page):
    """
    Custom Page Type — subclasses Wagtail's Page model.
    Uses StreamField for flexible block-based content.
    Exposed via Wagtail API v2 as a headless endpoint.
    """
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )
    excerpt = models.TextField(
        blank=True,
        help_text='Short description shown in article listings'
    )
    body = StreamField(
        [
            ('richtext', RichTextBlock(
                label='Rich Text',
                help_text='Formatted text block'
            )),
            ('image', ImageChooserBlock(
                label='Image',
                help_text='Upload or choose an image from the media library'
            )),
            ('quote', StructBlock(
                [
                    ('text', CharBlock(label='Quote text')),
                    ('author', CharBlock(label='Author', required=False)),
                ],
                label='Pull Quote'
            )),
        ],
        use_json_field=True,
        blank=True,
    )

    # Wagtail admin panels — what editors see in the CMS
    content_panels = Page.content_panels + [
        FieldPanel('category'),
        FieldPanel('excerpt'),
        FieldPanel('body'),
    ]

    # Fields exposed to Wagtail API v2
    api_fields = [
        APIField('category'),
        APIField('excerpt'),
        APIField('body'),
    ]

    class Meta:
        verbose_name = 'Article Page'
        verbose_name_plural = 'Article Pages'
