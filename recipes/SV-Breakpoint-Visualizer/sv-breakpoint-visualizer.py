# Description: A Gradio recipe to visualize structural variants with breakpoints in IGV.
# Note: Requires plotly to be installed. Install it using `pip install plotly`.

import argparse
import gradio as gr
from gradio_igv import IGV, IGVContext, AlignmentTrackLoad, VariantTrackLoad, parse_locus, FeatureContext
import pandas as pd
import pysam
import plotly.express as px


def parse_args():
    parser = argparse.ArgumentParser(description="Process SV VCF and BAM files for Gradio IGV demo.")
    parser.add_argument("--vcf-file", help="Path to the SV VCF file")
    parser.add_argument("--bam-file", help="Path to the BAM file")
    parser.add_argument("--insertion-types", default="INS", help="Comma-separated list of SV types to consider as inserted sequences")
    parser.add_argument("--sv-types", default="INS,DEL", help="Comma-separated list of SV types to consider")
    parser.add_argument("--start-at", default=None, help="Locus to start at, e.g. chr3:10000")
    return parser.parse_args()

def main():
    args = parse_args()

    start_at = args.start_at
    if start_at is not None:
        start_chrom, start_pos = start_at.split(':')
        var_iter = pysam.VariantFile(args.vcf_file).fetch(start_chrom, int(start_pos))
    else:
        var_iter = pysam.VariantFile(args.vcf_file).fetch()
    bam_file = args.bam_file
    ins_types = args.insertion_types.split(",")
    sv_types_opts = args.sv_types.split(",")

    def get_next_variant(sv_types: list[str]):
        for record in var_iter:
            if record.info["SVTYPE"] in sv_types:
                return record
        else:
            raise gr.Error("No more variants found for given types.")

    def jump_to_next_variant(igv_context: IGVContext, sv_types: list[str], padding: int):
        variant = get_next_variant(sv_types)
        if variant:
            left_locus = f"{variant.chrom}:{variant.pos - padding}-{variant.pos + padding}"
            right_locus = f"{variant.chrom}:{variant.stop - padding}-{variant.stop + padding}"
            if variant.info["SVTYPE"] in ins_types:
                new_locus = left_locus
            else:
                new_locus = f"{left_locus} {right_locus}"

            igv_context.update_locus(new_locus)
            variant_table = pd.DataFrame({
                "CHROM": [variant.chrom],
                "POS": [variant.pos],
                "END": [variant.stop],
                "SVTYPE": [variant.info["SVTYPE"]],
                "SVLEN": [variant.info["SVLEN"]],
                "GT": [variant.samples[0]["GT"]],
            })
        return igv_context, variant_table

    def slice_bq(read, lower_bound, upper_bound):
        i_min = []
        for i, x in enumerate(read.get_reference_positions()):
            if x < lower_bound:
                continue
            else:
                if x > upper_bound:
                    break
                else:
                    i_min += [i]

        if len(i_min) == 0:
            return []
        else:
            return list(read.query_qualities[i_min[0]:i_min[-1]])

    def get_visible_reads(igv_context: IGVContext):
        loci = parse_locus(igv_context.locus)
        if len(loci) == 2:
            left_locus, right_locus = loci
            left_features = FeatureContext(
                files=[bam_file],
                names=["left_reads"],
                loci=[left_locus],
            )

            right_features = FeatureContext(
                files=[bam_file],
                names=["right_reads"],
                loci=[right_locus],
            )

            left_df = pd.DataFrame({
                "Read Name": [read.query_name for read in left_features.features["left_reads"]],
                "MAPQ": [read.mapq for read in left_features.features["left_reads"]],
                "Breakpoint Side": ["Left"] * len(list(left_features.features["left_reads"])),
            })

            right_df = pd.DataFrame({
                "Read Name": [read.query_name for read in right_features.features["right_reads"]],
                "MAPQ": [read.mapq for read in right_features.features["right_reads"]],
                "Breakpoint Side": ["Right"] * len(list(right_features.features["right_reads"])),
            })

            read_summary_df = pd.concat([left_df, right_df])

            right_bq = [slice_bq(read, max(right_locus[1], read.get_reference_positions()[0]), min(right_locus[2], read.get_reference_positions()[-1])) for read in right_features.features["right_reads"]]
            right_bq = [item for sublist in right_bq for item in sublist]  # flatten the list
            left_bq = [slice_bq(read, max(left_locus[1], read.get_reference_positions()[0]), min(left_locus[2], read.get_reference_positions()[-1])) for read in left_features.features["left_reads"]]
            left_bq = [item for sublist in left_bq for item in sublist]  # flatten the list

            left_bq_df = pd.DataFrame({
                "BQ": left_bq,
                "Breakpoint Side": ["Left"] * len(left_bq),
            })

            right_bq_df = pd.DataFrame({
                "BQ": right_bq,
                "Breakpoint Side": ["Right"] * len(right_bq),
            })

            bq_df = pd.concat([left_bq_df, right_bq_df])
        else:
            features = FeatureContext(
                files=[bam_file],
                names=["reads"],
                loci=loci,
            )

            read_summary_df = pd.DataFrame({
                "Read Name": [read.query_name for read in features.features["reads"]],
                "MAPQ": [read.mapq for read in features.features["reads"]],
                "Breakpoint Side": ["Both"] * len(list(features.features["reads"])),
            })

            bq = [slice_bq(read, max(loci[0][1], read.get_reference_positions()[0]), min(loci[0][2], read.get_reference_positions()[-1])) for read in features.features["reads"]]
            bq = [item for sublist in bq for item in sublist]  # flatten the list
            bq_df = pd.DataFrame({
                "BQ": bq,
                "Breakpoint Side": ["Both"] * len(bq),
            })

        return read_summary_df, bq_df

    def plot_visible_reads(igv_context: IGVContext):
        summary_df, bq_df = get_visible_reads(igv_context)
        summary_fig = px.histogram(summary_df, x="MAPQ", color="Breakpoint Side", barmode="group")
        bq_fig = px.histogram(bq_df, x="BQ", color="Breakpoint Side", barmode="group")
        return summary_fig, bq_fig


    # Make initial IGVContext setup
    igv_context = IGVContext(
        genome="hg38",
    ).add_track(
        VariantTrackLoad(
            name="SVs",
            url=args.vcf_file,
        )
    ).add_track(
        AlignmentTrackLoad(
            name="Reads",
            url=bam_file,
            indexed=True,
            colorBy="strand"
        )
    )

    # Set up the UI
    with gr.Blocks(fill_height=True) as demo:
        with gr.Row(min_height=1000):
            with gr.Column(scale=3):
                with gr.Row():
                    padding_slider = gr.Slider(20, 150, 100, step=10, label="Padding Around Breakpoints")
                    sv_type_checklist = gr.CheckboxGroup(choices=sv_types_opts, value=sv_types_opts, label="SV Types")
                next_var_btn = gr.Button("Next Variant")
                variant_summary = gr.DataFrame(value=pd.DataFrame(), label="Variant Summary")
                igv_component = IGV(value=igv_context, label="IGV Browser")
            with gr.Column(scale=1):
                read_plot = gr.Plot(value=px.scatter(), label="Reads Plot",)
                bq_plot = gr.Plot(value=px.scatter(), label="Base Quality Plot",)

            next_var_btn.click(jump_to_next_variant, [igv_component, sv_type_checklist, padding_slider], [igv_component, variant_summary])

            igv_component.locuschange(plot_visible_reads, [igv_component], [read_plot, bq_plot])

    demo.launch()


if __name__ == "__main__":
    main()