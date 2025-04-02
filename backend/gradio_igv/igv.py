from gradio.components.base import Component
from gradio.events import EventListener
from gradio.data_classes import GradioModel
from pydantic import Field

from .data_types import *


class IGV(Component):
    """
    IGV Browser component.
    """

    EVENTS = [
        EventListener('trackremoved', doc="Triggered when a track is removed from the IGV Browser."),
        EventListener('trackdrag', doc="Triggered when a track is dragged in the IGV Browser."),
        EventListener('trackdragend', doc="Triggered when a track is finished being dragged in the IGV Browser."),
        EventListener('locuschange', doc="Triggered when the locus is changed in the IGV Browser."),
        EventListener('trackclick', doc="Triggered when a track is clicked in the IGV Browser."),
        EventListener('trackorderchanged', doc="Triggered when the order of tracks is changed in the IGV Browser.")
    ]

    data_model = IGVContext

    def preprocess(self, payload: IGVContext) -> IGVContext:
        """
        Passes through an IGVContext object to frontend.
        """
        return payload

    def postprocess(self, value: IGVContext) -> IGVContext:
        """
        Passes through an IGVContext object to backend.
        """
        return value

    def example_payload(self):
        return IGVContext(genome="hg38", locus="BRCA1")

    def example_value(self):
        return IGVContext(genome="hg38")
