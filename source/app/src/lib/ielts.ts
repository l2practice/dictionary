// Dữ liệu IELTS (Muse AI): collocation, ví dụ Writing/Speaking, mẹo — data/ielts.json, tải một lần khi cần.
export interface IeltsItem {
  pos: string; cefr: string; register: string; use: string; band: string;
  definition: string; vi: string; collocations: string[];
  writing_example: string; writing_vi: string; speaking_example: string; speaking_vi: string;
  tip: string; topics: string[];
}
let cache: Promise<Record<string, IeltsItem> | null> | null = null;
export function loadIelts(): Promise<Record<string, IeltsItem> | null> {
  if (!cache) {
    const base = ((import.meta.env.VITE_DATA_BASE as string) || "/data/") + "ielts.json";
    cache = fetch(new URL(base, location.href)).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  }
  return cache;
}
export async function ieltsOf(word: string): Promise<IeltsItem | null> {
  const d = await loadIelts();
  return d ? (d[word.toLowerCase()] ?? null) : null;
}

// Collocation cho từ phổ biến (Muse AI): data/collocations.json = {từ: {c: [cụm], e: ví dụ, v: dịch, n: ghi chú}}
export interface Colloc { c: ({ e: string; v: string } | string)[]; e: string; v: string; n: string }
let cc: Promise<Record<string, Colloc> | null> | null = null;
export function collocOf(word: string): Promise<Colloc | null> {
  if (!cc) {
    const base = ((import.meta.env.VITE_DATA_BASE as string) || "/data/") + "collocations.json";
    cc = fetch(new URL(base, location.href)).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  }
  return cc.then((d) => (d ? (d[word.toLowerCase()] ?? null) : null));
}
