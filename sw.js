const CACHE_NAME = 'snap-photo-edit-v17';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.png',
  './icon-192.png',
  './icon-512.png',
  './vendor/tailwindcss.js',
  './vendor/cropper.min.css',
  './vendor/cropper.min.js',
  './vendor/jspdf.umd.min.js',
  './vendor/jszip.min.js',
  './fonts/kanit.css',
  './fonts/kanit-300.ttf',
  './fonts/kanit-400.ttf',
  './fonts/kanit-500.ttf',
  './fonts/kanit-600.ttf',
  './fonts/kanit-700.ttf'
];

self.addEventListener('install', (e) => {
  self.skipWaiting(); // บังคับอัปเดตทันที
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(ASSETS.map((asset) => cache.add(asset)));
    })
  );
});

self.addEventListener('activate', (e) => {
  // ลบแคชเวอร์ชันเก่าทิ้งให้หมด จะได้ไม่เจอผีหลอก (โค้ดเก่าค้าง)
  e.waitUntil(
    caches.keys()
      .then((keyList) => {
        return Promise.all(keyList.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key); 
          }
        }));
      })
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method === 'POST') return; 
  if (!e.request.url.startsWith('http')) return;

  e.respondWith(
    caches.match(e.request).then((cachedRes) => {
      if (cachedRes) return cachedRes;

      return fetch(e.request).then((networkRes) => {
        if (networkRes && networkRes.ok) {
          const copy = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, copy));
        }
        return networkRes;
      }).catch(() => {
        if (e.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
        return Response.error();
      });
    })
  );
});
