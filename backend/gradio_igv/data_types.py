from typing import Optional, Dict
from gradio.data_classes import GradioModel
from gradio_client.exceptions import AuthenticationError
from pydantic import Field


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
    chromosomeOrder: Optional[list[str]] = Field(default=None)
    headers: Optional[Dict[str, str]] = Field(default=None)
    wholeGenomeView: bool = Field(default=True)

class TrackLoad(GradioModel):
    name: str
    url: str
    indexURL: Optional[str] = Field(default=None)
    indexed: bool = False
    order: Optional[int] = Field(default=None)
    height: int = 50
    autoHeight: bool = True
    minHeight: int = 50
    maxHeight: int = 500
    visibilityWindow: int = 30_000
    removable: bool = True
    headers: Optional[Dict[str, str]] = Field(default=None)
    oauthToken: Optional[str] = ""
    sourceType: Optional[str] = Field(default=None)
    # TODO: Add ROI

    def model_post_init(self, __context=None):
        # Set oauthToken to None in initialization to skip getting token
        if self.oauthToken is not None:
            self.get_oauth_token()

    def get_oauth_token(self):
        path_stem = self.url.removeprefix("https://").removeprefix("http://")
        if path_stem.startswith("gs://") or path_stem.startswith("google"):
            try:
                import google.auth
                from google.auth.transport.requests import Request

                creds, project_id = google.auth.default()

                # Refresh the credentials if they're expired
                if not creds.valid:
                    if creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        raise AuthenticationError("Google credentials are not valid and cannot be refreshed.")
                self.oauthToken = creds.token
            except Exception as e:
                print(f"Error getting Google credentials: {e}")
                return None

        elif path_stem.startswith("s3"):
            try:
                import boto3
                session = boto3.Session()
                sts_client = session.client("sts")
                response = sts_client.get_session_token()
                return response["Credentials"]["SessionToken"]
            except Exception as e:
                print(f"Error getting AWS token: {e}")
                return None

        elif path_stem.startswith("az://"):
            try:
                from azure.identity import DefaultAzureCredential
                credential = DefaultAzureCredential()
                token = credential.get_token("https://management.azure.com/.default")
                return token.token
            except Exception as e:
                print(f"Error getting Azure token: {e}")
                return None
        else:
            self.oauthToken = None

class VariantTrackLoad(TrackLoad):
    displayMode: Optional[str] = Field(default="EXPANDED", pattern="^(EXPANDED|SQUISHED|COLLAPSED)$")
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

class AlignmentSortOptions(GradioModel):
    chr: str
    position: int
    direction: Optional[str] = Field(default="ASC", pattern="^(ASC|DESC)$")
    option: str
    tag: Optional[str] = None

class AlignmentTrackLoad(TrackLoad):
    showCoverage: bool = True
    showAlignments: bool = True
    viewAsPairs: bool = False
    pairsSupported: bool = True
    coverageColor: Optional[str] = None
    color: str = "rgb(170, 170, 170)"
    deletionColor: str = "black"
    displayMode: str = Field(default="EXPANDED", pattern="^(FULL|EXPANDED|SQUISHED)$")
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

class AnnotationTrackLoad(TrackLoad):
    displayMode: str = Field(default="COLLAPSED", pattern="^(EXPANDED|SQUISHED|COLLAPSED)$")
    squishedRowHeight: int = 15
    expandedRowHeight: int = 30
    color: str = "rgb(0,0,150)"
    colorBy: Optional[str] = None
    altColor: Optional[str] = None
    colorTable: Optional[Dict[str, str]] = None
    searchable: bool = False
    searchableFields: list[str] = Field(default_factory=list)
    nameField: Optional[str] = None
    maxRows: int = 500
    filterTypes: Optional[list[str]] = None


class IGVContext(GradioModel):
    """
    IGV Browser context object. Should be initialized by setting only the `genome` and `locus` fields. Uploading and removing tracks should be handled by the convenience methods `update_genome`, `add_track`, and `remove_track`.
    """
    genome: str | ReferenceGenome = Field(default="hg38")
    locus: str = Field(default="")
    loadAlignmentTracks: list[AlignmentTrackLoad] = Field(default_factory=list)
    loadVariantTracks: list[VariantTrackLoad] = Field(default_factory=list)
    loadAnnotationTracks: list[AnnotationTrackLoad] = Field(default_factory=list)
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
            raise ValueError("TrackLoad type not recognized.")

        return self

    def remove_track(self, track: str):
        self.removeTracks.append(track)
        return self
