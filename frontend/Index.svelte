<script lang="ts">
  import { onMount } from "svelte";
  import igv from "igv";
  import type { ReferenceGenome, TrackType, TrackLoad } from "igv";
  import type { CreateOpt, Browser } from "igv";
  import { Gradio } from "@gradio/utils";
  import { debounce } from "./utils";

  import { Block, Info } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";
  import type { SelectData } from "@gradio/utils";

  import type { IGVContext } from "./IGVContext";
  import { roundLocus } from "./IGVContext";

  export let value: IGVContext;  // Passed from Gradio backend
  let prevGenome: string | ReferenceGenome;
  let prevLocus: string;

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let container = true;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let loading_status: LoadingStatus;
  export let gradio: Gradio<{
    change: never;
    select: SelectData;
    input: never;
    clear_status: LoadingStatus;
  }>;

  export let locusChangeCooldown = 300; // Cooldown in ms for locus change events

  let default_value: IGVContext = {
    genome: "hg38",
    locus: "",
    loadAlignmentTracks: [],
    loadVariantTracks: [],
    loadAnnotationTracks: [],
    removeTracks: [],
  }

  let igvDiv: HTMLDivElement;
  let browser: Browser;

  // Handle the lifecycle of the IGV browser
  onMount(async () => {
    const options: CreateOpt = {
      genome: "hg38",  // Default genome
      locus: value.locus as string,    // Initial locus value passed from Gradio
    };
    browser = await igv.createBrowser(igvDiv, options);

    // Forward IGV browser events to Gradio
    browser.on("trackremoved", () => {
      gradio.dispatch("trackremoved");
    });

    browser.on("trackdrag", () => {
      gradio.dispatch("trackdrag");
    });

    browser.on("trackdragend", () => {
      gradio.dispatch("trackdragend");
      value.locus = roundLocus(browser.currentLoci());
    });

    browser.on("locuschange", debounce(() => {
      gradio.dispatch("locuschange");
      value.locus = roundLocus(browser.currentLoci());
    }, locusChangeCooldown));

    browser.on("trackclick", () => {
      gradio.dispatch("trackclick");
      return true;
    });

    browser.on("trackorderchanged", () => {
      gradio.dispatch("trackorderchanged");
    });

    // value = default_value;
    prevGenome = value.genome;
    prevLocus = value.locus;
  });

  // Utilities to handle updating state when value changes
  let updateLocus = (locus: string) => {
    browser.search(locus);
    prevLocus = locus;
  };

  let updateGenome = (genome: string | ReferenceGenome) => {
    browser.loadGenome(genome).then(() => {
      updateLocus(value.locus);
    });
    prevGenome = genome;
  };

  let loadedTracks = new Set<string>();
  let addTracks = async (tracks: TrackLoad<TrackType>[]) => {
    // Check which tracks are not already loaded
    let newTracks = tracks.filter((track) => !loadedTracks.has(track.name!));
    if (newTracks.length === 0) return; // No new tracks to load

    // Load the new tracks
    await Promise.all(newTracks.map( (track) => browser.loadTrack(track) ));
    newTracks.forEach((track) => loadedTracks.add(track.name!));
    tracks.length = 0;
  }

  let removeTracks = async (tracks: string[]) => {
    await Promise.all(tracks.map( (track) => browser.removeTrackByName(track) ));
    tracks.forEach((track) => loadedTracks.delete(track));
    tracks.length = 0;
  }

  // Update the IGV browser when the value changes
  $: if (browser && value) {
    if (prevLocus !== value.locus) {
      updateLocus(value.locus);
    }

    if (prevGenome !== value.genome) {
      updateGenome(value.genome);
    }

    if (value.loadAlignmentTracks.length > 0) {
      addTracks(value.loadAlignmentTracks);
    }

    if (value.loadVariantTracks.length > 0) {
      addTracks(value.loadVariantTracks);
    }

    if (value.loadAnnotationTracks.length > 0) {
      addTracks(value.loadAnnotationTracks);
    }

    if (value.removeTracks.length > 0) {
      removeTracks(value.removeTracks);
    }
  }


</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
  {#if loading_status}
    <StatusTracker
      autoscroll={gradio.autoscroll}
      i18n={gradio.i18n}
      {...loading_status}
      on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
    />
  {/if}
  <div class="igv-container" bind:this={igvDiv}></div>
</Block>

<style>
  .igv-container {
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 10px;
    width: 100%;
    height: 100%;
    background-color: #ffffff;
    color: #000000;
  }
</style>
