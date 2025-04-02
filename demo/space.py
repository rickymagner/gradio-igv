
import gradio as gr
from app import demo as app
import os

_docs = {'IGV': {'description': 'IGV Browser component.', 'members': {'__init__': {'value': {'type': 'Any', 'default': 'None', 'description': None}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'info': {'type': 'str | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': None}, 'container': {'type': 'bool', 'default': 'True', 'description': None}, 'scale': {'type': 'int | None', 'default': 'None', 'description': None}, 'min_width': {'type': 'int | None', 'default': 'None', 'description': None}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': None}, 'visible': {'type': 'bool', 'default': 'True', 'description': None}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': None}, 'render': {'type': 'bool', 'default': 'True', 'description': None}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': None}, 'load_fn': {'type': 'Callable | None', 'default': 'None', 'description': None}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': None}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': None}}, 'postprocess': {'value': {'type': 'IGVContext', 'description': None}}, 'preprocess': {'return': {'type': 'IGVContext', 'description': None}, 'value': None}}, 'events': {'trackremoved': {'type': None, 'default': None, 'description': 'Triggered when a track is removed from the IGV Browser.'}, 'trackdrag': {'type': None, 'default': None, 'description': 'Triggered when a track is dragged in the IGV Browser.'}, 'trackdragend': {'type': None, 'default': None, 'description': 'Triggered when a track is finished being dragged in the IGV Browser.'}, 'locuschange': {'type': None, 'default': None, 'description': 'Triggered when the locus is changed in the IGV Browser.'}, 'trackclick': {'type': None, 'default': None, 'description': 'Triggered when a track is clicked in the IGV Browser.'}, 'trackorderchanged': {'type': None, 'default': None, 'description': 'Triggered when the order of tracks is changed in the IGV Browser.'}}}, '__meta__': {'additional_interfaces': {'IGVContext': {'source': 'class IGVContext(GradioModel):\n    genome: str | ReferenceGenome = Field(default="hg38")\n    locus: str = Field(default="")\n    loadAlignmentTracks: list[AlignmentTrackLoad] = Field(\n        default_factory=list\n    )\n    loadVariantTracks: list[VariantTrackLoad] = Field(\n        default_factory=list\n    )\n    loadAnnotationTracks: list[AnnotationTrackLoad] = Field(\n        default_factory=list\n    )\n    removeTracks: list[str] = Field(default_factory=list)\n\n    def update_genome(self, genome: str | ReferenceGenome):\n        self.genome = genome\n        return self\n\n    def update_locus(self, locus: str):\n        self.locus = locus\n        return self\n\n    def add_track(self, track_load: TrackLoad):\n        if isinstance(track_load, AlignmentTrackLoad):\n            self.loadAlignmentTracks.append(track_load)\n        elif isinstance(track_load, VariantTrackLoad):\n            self.loadVariantTracks.append(track_load)\n        elif isinstance(track_load, AnnotationTrackLoad):\n            self.loadAnnotationTracks.append(track_load)\n        else:\n            raise ValueError(\n                "TrackLoad type not recognized."\n            )\n\n        return self\n\n    def remove_track(self, track: str):\n        self.removeTracks.append(track)\n        return self', 'refs': ['ReferenceGenome', 'AlignmentTrackLoad', 'VariantTrackLoad', 'AnnotationTrackLoad']}, 'ReferenceGenome': {'source': 'class ReferenceGenome(GradioModel):\n    id: Optional[str] = Field(default="hg38")\n    name: Optional[str] = Field(default="hg38")\n    fastaURL: Optional[str] = Field(default=None)\n    indexURL: Optional[str] = Field(default=None)\n    compressedIndexURL: Optional[str] = Field(default=None)\n    twoBitURL: Optional[str] = Field(default=None)\n    cytobandURL: Optional[str] = Field(default=None)\n    aliasURL: Optional[str] = Field(default=None)\n    chromSizesURL: Optional[str] = Field(default=None)\n    chromosomeOrder: Optional[list[str]] = Field(\n        default=None\n    )\n    headers: Optional[Dict[str, str]] = Field(default=None)\n    wholeGenomeView: bool = Field(default=True)'}, 'AlignmentTrackLoad': {'source': 'class AlignmentTrackLoad(TrackLoad):\n    showCoverage: bool = True\n    showAlignments: bool = True\n    viewAsPairs: bool = False\n    pairsSupported: bool = True\n    coverageColor: Optional[str] = None\n    color: str = "rgb(170, 170, 170)"\n    deletionColor: str = "black"\n    displayMode: str = Field(\n        default="EXPANDED",\n        pattern="^(FULL|EXPANDED|SQUISHED)$",\n    )\n    groupBy: Optional[str] = None\n    samplingWindowSize: int = 100\n    samplingDepth: int = 100\n    readGroup: Optional[str] = None\n    sort: Optional[AlignmentSortOptions] = None\n    filter: Dict[str, bool | int | list[str]] = None\n    showSoftClips: bool = False\n    showMismatches: bool = True\n    showAllBases: bool = False\n    showInsertionText: bool = False\n    insertionTextColor: str = "white"\n    alignmentRowHeight: int = 14\n    squishedRowHeight: int = 3\n    colorBy: str = "unexpectedPair"\n    insertionColor: str = "rgb(138, 94, 161)"\n    negStrandColor: str = "rgba(150, 150, 230, 0.75)"', 'refs': ['AlignmentSortOptions']}, 'AlignmentSortOptions': {'source': 'class AlignmentSortOptions(GradioModel):\n    chr: str\n    position: int\n    direction: Optional[str] = Field(\n        default="ASC", pattern="^(ASC|DESC)$"\n    )\n    option: str\n    tag: Optional[str] = None'}, 'VariantTrackLoad': {'source': 'class VariantTrackLoad(TrackLoad):\n    displayMode: Optional[str] = Field(\n        default="EXPANDED",\n        pattern="^(EXPANDED|SQUISHED|COLLAPSED)$",\n    )\n    squishedCallHeight: Optional[int] = 1\n    expandedCallHeight: Optional[int] = 10\n    color: Optional[str] = None\n    colorBy: Optional[str] = None\n    colorTable: Optional[Dict[str, str]] = None\n    noCallColor: Optional[str] = "rgb(250, 250, 250)"\n    homvarColor: Optional[str] = "rgb(17,248,254)"\n    hetvarColor: Optional[str] = "rgb(34,12,253)"\n    homrefColor: Optional[str] = "rgb(200, 200, 200)"\n    supportsWholeGenome: Optional[bool] = None\n    showGenotypes: Optional[bool] = None\n    # strokecolor: Optional[Callable[[VCFItem], str]] = None\n    # context_hook: Optional[Callable[[VCFItem, Draw.CanvasContext, int, int, int, int], None]] = None'}, 'AnnotationTrackLoad': {'source': 'class AnnotationTrackLoad(TrackLoad):\n    displayMode: str = Field(\n        default="COLLAPSED",\n        pattern="^(EXPANDED|SQUISHED|COLLAPSED)$",\n    )\n    squishedRowHeight: int = 15\n    expandedRowHeight: int = 30\n    color: str = "rgb(0,0,150)"\n    colorBy: Optional[str] = None\n    altColor: Optional[str] = None\n    colorTable: Optional[Dict[str, str]] = None\n    searchable: bool = False\n    searchableFields: list[str] = Field(\n        default_factory=list\n    )\n    nameField: Optional[str] = None\n    maxRows: int = 500\n    filterTypes: Optional[list[str]] = None'}}, 'user_fn_refs': {'IGV': ['IGVContext']}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_igv`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Embed IGV.js in your app to visualize genomics data.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_igv
```

## Usage

```python
import gradio as gr
from gradio_igv import IGV, IGVContext, AlignmentTrackLoad, FeatureContext, parse_locus
import pandas as pd


public_cram = "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram"
default_igv_context = IGVContext(
    genome="hg38",
).update_locus("BRCA1").add_track(
    AlignmentTrackLoad(
        name="HG00103",
        url=public_cram,
        indexURL=f"{public_cram}.crai",
        order=1,
        height=200,
        colorBy="strand",
        oauthToken=None,  # Public file so no auth needed; otherwise inferred by URL type using environment
    )
)

def summarize_visible_alignments(igv_context):
    loci = parse_locus(igv_context.locus)
    feature_ctx = FeatureContext(
        files=[public_cram],
        names=["HG00103"],
        loci=loci,
    )

    reads = list(feature_ctx.features["HG00103"])
    df = pd.DataFrame({
        "Read Name": [read.query_name for read in reads],
        "Pos": [read.reference_start for read in reads],
        "MAPQ": [read.mapq for read in reads],
    }).sort_values(by='Pos')
    return df.head(20)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            igv_component = IGV(value=default_igv_context, label="IGV Browser")
        with gr.Column(scale=1):
            alignment_summary = gr.DataFrame(value=pd.DataFrame(), label="Alignment Summary", max_height=800)

    igv_component.locuschange(summarize_visible_alignments, [igv_component], [alignment_summary])

if __name__ == "__main__":
    demo.launch()
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `IGV`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["IGV"]["members"]["__init__"], linkify=['IGVContext', 'ReferenceGenome', 'AlignmentTrackLoad', 'AlignmentSortOptions', 'VariantTrackLoad', 'AnnotationTrackLoad'])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["IGV"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: IGVContext
) -> IGVContext:
    return value
```
""", elem_classes=["md-custom", "IGV-user-fn"], header_links=True)




    code_IGVContext = gr.Markdown("""
## `IGVContext`
```python
class IGVContext(GradioModel):
    genome: str | ReferenceGenome = Field(default="hg38")
    locus: str = Field(default="")
    loadAlignmentTracks: list[AlignmentTrackLoad] = Field(
        default_factory=list
    )
    loadVariantTracks: list[VariantTrackLoad] = Field(
        default_factory=list
    )
    loadAnnotationTracks: list[AnnotationTrackLoad] = Field(
        default_factory=list
    )
    removeTracks: list[str] = Field(default_factory=list)

    def update_genome(self, genome: str | ReferenceGenome):
        self.genome = genome
        return self

    def update_locus(self, locus: str):
        self.locus = locus
        return self

    def add_track(self, track_load: TrackLoad):
        if isinstance(track_load, AlignmentTrackLoad):
            self.loadAlignmentTracks.append(track_load)
        elif isinstance(track_load, VariantTrackLoad):
            self.loadVariantTracks.append(track_load)
        elif isinstance(track_load, AnnotationTrackLoad):
            self.loadAnnotationTracks.append(track_load)
        else:
            raise ValueError(
                "TrackLoad type not recognized."
            )

        return self

    def remove_track(self, track: str):
        self.removeTracks.append(track)
        return self
```""", elem_classes=["md-custom", "IGVContext"], header_links=True)

    code_ReferenceGenome = gr.Markdown("""
## `ReferenceGenome`
```python
class ReferenceGenome(GradioModel):
    id: Optional[str] = Field(default="hg38")
    name: Optional[str] = Field(default="hg38")
    fastaURL: Optional[str] = Field(default=None)
    indexURL: Optional[str] = Field(default=None)
    compressedIndexURL: Optional[str] = Field(default=None)
    twoBitURL: Optional[str] = Field(default=None)
    cytobandURL: Optional[str] = Field(default=None)
    aliasURL: Optional[str] = Field(default=None)
    chromSizesURL: Optional[str] = Field(default=None)
    chromosomeOrder: Optional[list[str]] = Field(
        default=None
    )
    headers: Optional[Dict[str, str]] = Field(default=None)
    wholeGenomeView: bool = Field(default=True)
```""", elem_classes=["md-custom", "ReferenceGenome"], header_links=True)

    code_AlignmentTrackLoad = gr.Markdown("""
## `AlignmentTrackLoad`
```python
class AlignmentTrackLoad(TrackLoad):
    showCoverage: bool = True
    showAlignments: bool = True
    viewAsPairs: bool = False
    pairsSupported: bool = True
    coverageColor: Optional[str] = None
    color: str = "rgb(170, 170, 170)"
    deletionColor: str = "black"
    displayMode: str = Field(
        default="EXPANDED",
        pattern="^(FULL|EXPANDED|SQUISHED)$",
    )
    groupBy: Optional[str] = None
    samplingWindowSize: int = 100
    samplingDepth: int = 100
    readGroup: Optional[str] = None
    sort: Optional[AlignmentSortOptions] = None
    filter: Dict[str, bool | int | list[str]] = None
    showSoftClips: bool = False
    showMismatches: bool = True
    showAllBases: bool = False
    showInsertionText: bool = False
    insertionTextColor: str = "white"
    alignmentRowHeight: int = 14
    squishedRowHeight: int = 3
    colorBy: str = "unexpectedPair"
    insertionColor: str = "rgb(138, 94, 161)"
    negStrandColor: str = "rgba(150, 150, 230, 0.75)"
```""", elem_classes=["md-custom", "AlignmentTrackLoad"], header_links=True)

    code_AlignmentSortOptions = gr.Markdown("""
## `AlignmentSortOptions`
```python
class AlignmentSortOptions(GradioModel):
    chr: str
    position: int
    direction: Optional[str] = Field(
        default="ASC", pattern="^(ASC|DESC)$"
    )
    option: str
    tag: Optional[str] = None
```""", elem_classes=["md-custom", "AlignmentSortOptions"], header_links=True)

    code_VariantTrackLoad = gr.Markdown("""
## `VariantTrackLoad`
```python
class VariantTrackLoad(TrackLoad):
    displayMode: Optional[str] = Field(
        default="EXPANDED",
        pattern="^(EXPANDED|SQUISHED|COLLAPSED)$",
    )
    squishedCallHeight: Optional[int] = 1
    expandedCallHeight: Optional[int] = 10
    color: Optional[str] = None
    colorBy: Optional[str] = None
    colorTable: Optional[Dict[str, str]] = None
    noCallColor: Optional[str] = "rgb(250, 250, 250)"
    homvarColor: Optional[str] = "rgb(17,248,254)"
    hetvarColor: Optional[str] = "rgb(34,12,253)"
    homrefColor: Optional[str] = "rgb(200, 200, 200)"
    supportsWholeGenome: Optional[bool] = None
    showGenotypes: Optional[bool] = None
    # strokecolor: Optional[Callable[[VCFItem], str]] = None
    # context_hook: Optional[Callable[[VCFItem, Draw.CanvasContext, int, int, int, int], None]] = None
```""", elem_classes=["md-custom", "VariantTrackLoad"], header_links=True)

    code_AnnotationTrackLoad = gr.Markdown("""
## `AnnotationTrackLoad`
```python
class AnnotationTrackLoad(TrackLoad):
    displayMode: str = Field(
        default="COLLAPSED",
        pattern="^(EXPANDED|SQUISHED|COLLAPSED)$",
    )
    squishedRowHeight: int = 15
    expandedRowHeight: int = 30
    color: str = "rgb(0,0,150)"
    colorBy: Optional[str] = None
    altColor: Optional[str] = None
    colorTable: Optional[Dict[str, str]] = None
    searchable: bool = False
    searchableFields: list[str] = Field(
        default_factory=list
    )
    nameField: Optional[str] = None
    maxRows: int = 500
    filterTypes: Optional[list[str]] = None
```""", elem_classes=["md-custom", "AnnotationTrackLoad"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
            IGVContext: ['ReferenceGenome', 'AlignmentTrackLoad', 'VariantTrackLoad', 'AnnotationTrackLoad'], 
            ReferenceGenome: [], 
            AlignmentTrackLoad: ['AlignmentSortOptions'], 
            AlignmentSortOptions: [], 
            VariantTrackLoad: [], 
            AnnotationTrackLoad: [], };
    const user_fn_refs = {
          IGV: ['IGVContext'], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
