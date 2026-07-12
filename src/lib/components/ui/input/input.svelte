<script lang="ts">
	import type { HTMLInputAttributes, HTMLInputTypeAttribute } from "svelte/elements";
	import { cn, type WithElementRef } from "$lib/utils/cn.js";

	type InputType = Exclude<HTMLInputTypeAttribute, "file">;

	type Props = WithElementRef<
		Omit<HTMLInputAttributes, "type"> &
			({ type: "file"; files?: FileList } | { type?: InputType; files?: undefined })
	>;

	let {
		ref = $bindable(null),
		value = $bindable(),
		type,
		files = $bindable(),
		class: className,
		"data-slot": dataSlot = "input",
		...restProps
	}: Props = $props();
</script>

{#if type === "file"}
	<input
		bind:this={ref}
		data-slot={dataSlot}
		class={cn(
			"h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3 py-1.5 text-sm text-[var(--text-primary)] transition-all file:mr-3 file:rounded-lg file:border-0 file:bg-burgundy-50 dark:file:bg-burgundy-950 file:px-3 file:py-1 file:text-xs file:font-semibold file:text-burgundy-700 dark:file:text-gold-400 focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 disabled:cursor-not-allowed disabled:opacity-50",
			className
		)}
		type="file"
		bind:files
		bind:value
		{...restProps}
	/>
{:else}
	<input
		bind:this={ref}
		data-slot={dataSlot}
		class={cn(
			"h-10 w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] transition-all focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 disabled:cursor-not-allowed disabled:opacity-50",
			className
		)}
		{type}
		bind:value
		{...restProps}
	/>
{/if}
