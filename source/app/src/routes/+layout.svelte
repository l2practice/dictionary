<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";
  let { children } = $props();
  onMount(() => document.getElementById("boot")?.remove());
</script>

{@render children()}
