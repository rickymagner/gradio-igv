import pysam
from itertools import chain


def parse_locus(locus: str):
    if ':' not in locus:
        raise ValueError("Locus must be in the format 'chrom:start-end' or space-delimited list of such.")
    loci = []
    for l in locus.split(' '):
        chrom, pos = l.split(':')
        start, end = pos.split('-')
        loci.append((chrom, int(start), int(end)))
    return loci

class FeatureContext:
    def __init__(self, files: list[str], names: list[str], loci: list[tuple[str, int, int]]):
        self.files = files
        self.loci = loci
        self.names = names
        self.file_names = dict(zip(files, names))

        self.loaded_files = {}
        self.features = {}

        for file in self.files:
            if file.endswith(".bam") or file.endswith(".cram"):
                self.loaded_files[self.file_names[file]] = pysam.AlignmentFile(file, "rb")
            if file.endswith(".vcf") or file.endswith(".bcf") or file.endswith(".vcf.gz"):
                self.loaded_files[self.file_names[file]] = pysam.VariantFile(file)
            if file.endswith(".fasta") or file.endswith(".fa") or file.endswith(".fna") or file.endswith(".fasta.gz") or file.endswith(".fa.gz") or file.endswith(".fna.gz"):
                self.loaded_files[self.file_names[file]] = pysam.FastaFile(file)
            if file.endswith(".bed.gz"):
                self.loaded_files[self.file_names[file]] = pysam.TabixFile(file)

        self.get_features()

    def get_features(self):
        for name, file in self.loaded_files.items():
            if isinstance(file, pysam.AlignmentFile) or isinstance(file, pysam.VariantFile):
                self.features[name] = []
                for feature in chain.from_iterable([file.fetch(*locus) for locus in self.loci]):
                    self.features[name].append(feature)
            if isinstance(file, pysam.FastaFile):
                self.features[name] = [file.fetch(*locus) for locus in self.loci]

