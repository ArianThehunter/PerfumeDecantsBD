<script lang="ts">
	import { cn, type WithElementRef, type WithoutChildren } from "$lib/utils/cn.js";
	import type { HTMLTextareaAttributes } from "svelte/elements";

	let {
		ref = $bindable(null),
		value = $bindable(),
		class: className,
		"data-slot": dataSlot = "textarea",
		...restProps
	}: WithoutChildren<WithElementRef<HTMLTextareaAttributes>> = $props();
</script>

<textarea
	bind:this={ref}
	data-slot={dataSlot}
	class={cn(
		"w-full rounded-xl border border-gray-300 dark:border-gray-800 bg-white dark:bg-gray-900 px-3.5 py-2.5 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] transition-all focus:outline-none focus:border-burgundy-600 focus:ring-2 focus:ring-burgundy-500/20 dark:focus:border-gold-500 dark:focus:ring-gold-500/20 disabled:cursor-not-allowed disabled:opacity-50 min-h-24",
		className
	)}
	bind:value
	{...restProps}
></textarea>
