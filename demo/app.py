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