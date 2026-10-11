/// <reference lib="webworker" />
// Bộ nhớ đệm để mở ứng dụng gần như tức thì từ lần thứ hai (và dùng được khi mất mạng):
//  - vỏ ứng dụng (index.html, JS, CSS, font, logo): tải sẵn một lần theo từng phiên bản, lấy từ máy ngay khi mở;
//  - dữ liệu từ điển (data/…): trả từ máy ngay, đồng thời tải bản mới ở nền cho lần sau (stale-while-revalidate).
import { base, build, files, version } from "$service-worker";

const sw = self as unknown as ServiceWorkerGlobalScope;
const SHELL = `shell-${version}`;
const DATA = "data-v1";
const INDEX = `${base}/index.html`;
const PRECACHE = [INDEX, ...build, ...files.filter((f) => !f.endsWith(".json") && !f.endsWith(".txt"))];

sw.addEventListener("install", (e) => {
  e.waitUntil(
    caches
      .open(SHELL)
      .then((c) => c.addAll(PRECACHE))
      .then(() => sw.skipWaiting()),
  );
});

sw.addEventListener("activate", (e) => {
  e.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("shell-") && k !== SHELL).map((k) => caches.delete(k))))
      .then(() => sw.clients.claim()),
  );
});

async function staleWhileRevalidate(e: FetchEvent, req: Request): Promise<Response> {
  const cache = await caches.open(DATA);
  const hit = await cache.match(req);
  const net = fetch(req)
    .then(async (r) => {
      if (r.ok) await cache.put(req, r.clone());
      return r;
    })
    .catch(() => null);
  if (hit) {
    e.waitUntil(net); // làm mới ở nền cho lần mở sau
    return hit;
  }
  return (await net) ?? new Response("offline", { status: 503 });
}

sw.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== sw.location.origin || !url.pathname.startsWith(base + "/")) return;

  if (req.mode === "navigate") {
    // mọi đường dẫn của ứng dụng là một trang (định tuyến bằng "#"): trả index.html của phiên bản hiện tại
    e.respondWith(caches.open(SHELL).then((c) => c.match(INDEX)).then((r) => r ?? fetch(req)));
    return;
  }
  if (url.pathname.startsWith(base + "/data/")) {
    // manifest.json: worker xin với cache:"no-cache"; vẫn trả bản máy trước, nền làm mới
    e.respondWith(staleWhileRevalidate(e, new Request(url.origin + url.pathname)));
    return;
  }
  e.respondWith(caches.open(SHELL).then((c) => c.match(req)).then((r) => r ?? fetch(req)));
});
