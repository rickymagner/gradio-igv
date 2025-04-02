import type {ReferenceGenome, TrackType, TrackLoad, TypeFormatPair} from "igv";
import type { Tracks } from "igv";

type AlignmentTrackLoad = Tracks.TrackCommonOptions & Tracks.AlignmentTrackOptions & TypeFormatPair<'alignment'>;
type VariantTrackLoad = Tracks.TrackCommonOptions & Tracks.VariantTrackOptions & TypeFormatPair<'variant'>;
type AnnotationTrackLoad = Tracks.TrackCommonOptions & Tracks.AnnotationTrackOptions & TypeFormatPair<'annotation'>;

export interface IGVContext {
    genome: string | ReferenceGenome;
    locus: string;
    loadAlignmentTracks: AlignmentTrackLoad[];
    loadVariantTracks: VariantTrackLoad[];
    loadAnnotationTracks: AnnotationTrackLoad[];
    removeTracks: string[];
}

let roundSingleLocus = (locus: string) => {
    if (!locus.includes(":")) {
        return locus;
    }
    let [chr, startEnd] = locus.split(":");
    let [startFloat, endFloat] = startEnd.split("-");
    let start = Math.ceil(parseInt(startFloat));
    let end = Math.ceil(parseInt(endFloat));
    return `${chr}:${start}-${end}`;
};

export let roundLocus = (locus: string | string[]) => {
    // Split on whitespace and then parse the locus in chr:start-end format rounding start and end
    if (typeof locus === "string") {
        return roundSingleLocus(locus);
    } else {
        return locus.map(roundSingleLocus).join(" ");
    }
};
