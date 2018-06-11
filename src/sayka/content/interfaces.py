# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from sayka.content import _
from zope import schema
from plone.app.textfield import RichText
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.supermodel.directives import fieldset


class ISaykaContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IStory(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )
    question = schema.Text(
        title=(u'Question'),
        required=True
    )
    answer = schema.Text(
        title=_(u'Answer'),
        required=True
    )


class IYoutube(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    description = schema.Text(
        title=(u'Description'),
        required=False
    )

    url = schema.Text(
        title=(u'url'),
        required=True
    )


class INews(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    description = schema.Text(
        title=(u'Description'),
        required=False
    )

    cover = NamedBlobImage(
        title=_(u"Cover Image."),
        description=_(u"Cover image."),
        required=False,
    )



class IProduct(Interface):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    detail = schema.Text(
        title=_(u'Detail for product'),
        required=False
    )
    sale_price = schema.Int(
        title=_(u"Sale price"),
        description=_(u"Sale price for the product"),
        required=True,
    )
    cover = NamedBlobImage(
        title=_(u"Cover Image."),
        description=_(u"Cover image."),
        required=False,
    )

    image_1 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image for header."),
        required=False,
    )

    image_2 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_3 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_4 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_5 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image for header."),
        required=False,
    )

    image_6 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_7 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

    image_8 = NamedBlobImage(
        title=_(u"Product Image."),
        description=_(u"Product image."),
        required=False,
    )

class ICover(Interface):
    title = schema.TextLine(
        title=_(u'Title'),
        required=True
    )

    banner1_title = schema.TextLine(
        title=_(u'Banner1 Title'),
        required=True
    )
    description1 = RichText(
        title=_(u"Dsecription1"),
        required=False,
    )
    banner1 = NamedBlobImage(
        title=_(u"Banner1 Image."),
        required=False,
    )

    banner2_title = schema.TextLine(
        title=_(u'Banner2 Title'),
        required=True
    )
    description2 = RichText(
        title=_(u"Dsecription2"),
        required=False
    )
    banner2 = NamedBlobImage(
        title=_(u"Banner2 Image."),
        required=False,
    )

    banner3_title = schema.TextLine(
        title=_(u'Banner3 Title'),
        required=True
    )
    description3 = RichText(
        title=_(u"Dsecription3"),
        required=False,
    )
    banner3 = NamedBlobImage(
        title=_(u"Banner3 Image."),
        description=_(u"Banner image."),
        required=False,
    )

    banner4_title = schema.TextLine(
        title=_(u'Banner4 Title'),
        required=True
    )
    description4 = RichText(
        title=_(u"Dsecription4"),
        required=False,
    )
    banner4 = NamedBlobImage(
        title=_(u"Banner4 Image."),
        description=_(u"Banner image."),
        required=False,
    )

    banner5_title = schema.TextLine(
        title=_(u'Banner5 Title'),
        required=True
    )
    description5 = RichText(
        title=_(u"Dsecription5"),
        required=False
    )
    banner5 = NamedBlobImage(
        title=_(u"Banner5 Image."),
        description=_(u"Banner image."),
        required=False,
    )

    fieldset(_(u'Cover Background Images'),
             fields=['bg_1', 'bg_2'])
    bg_1 = NamedBlobImage(
        title=_(u'Background image 1'),
        required=True,
    )
    bg_2 = NamedBlobImage(
        title=_(u'Background image 2'),
        required=True,
    )

    fieldset(_(u'Cover Footer Slider'),
             fields=['f_slider_1', 'f_slider_desc_1',
                     'f_slider_2', 'f_slider_desc_2',
                     'f_slider_3', 'f_slider_desc_3',
                     'f_slider_4', 'f_slider_desc_4',])
    f_slider_1 = NamedBlobImage(
        title=_(u"Footer Slider."),
        required=True,
    )
    f_slider_desc_1 = schema.TextLine(
        title=_(u'Footer Slider Description'),
        required=True
    )

    f_slider_2 = NamedBlobImage(
        title=_(u"Footer Slider."),
        required=True,
    )
    f_slider_desc_2 = schema.TextLine(
        title=_(u'Footer Slider Description'),
        required=True
    )

    f_slider_3 = NamedBlobImage(
        title=_(u"Footer Slider."),
        required=True,
    )
    f_slider_desc_3 = schema.TextLine(
        title=_(u'Footer Slider Description'),
        required=True
    )

    f_slider_4 = NamedBlobImage(
        title=_(u"Footer Slider."),
        required=True,
    )
    f_slider_desc_4 = schema.TextLine(
        title=_(u'Footer Slider Description'),
        required=True
    )



