/* Tự chữa khi ứng dụng không khởi động được (thường do bộ nhớ đệm của phiên bản cũ sau khi cập nhật):
   nếu sau 10 giây màn hình chờ (#boot) vẫn còn, xoá service worker + bộ nhớ đệm vỏ ứng dụng rồi tải lại một lần.
   Dữ liệu từ điển (cache "data-v1") và danh sách từ của người dùng được giữ nguyên. */
(function () {
  var KEY = "dict-boot-heal";
  setTimeout(function () {
    var boot = document.getElementById("boot");
    if (!boot) return;
    var tried = 0;
    try { tried = +(sessionStorage.getItem(KEY) || 0); } catch (e) {}
    if (tried >= 1) {
      var m = document.createElement("span");
      m.textContent = "Không tải được ứng dụng. Hãy tải lại trang hoặc xoá dữ liệu trang web.";
      m.style.cssText = "max-width:300px;text-align:center;font-size:13px;opacity:.8";
      boot.appendChild(m);
      return;
    }
    try { sessionStorage.setItem(KEY, String(tried + 1)); } catch (e) {}
    var jobs = [];
    if (navigator.serviceWorker && navigator.serviceWorker.getRegistrations)
      jobs.push(navigator.serviceWorker.getRegistrations().then(function (rs) { return Promise.all(rs.map(function (r) { return r.unregister(); })); }));
    if (window.caches)
      jobs.push(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k.indexOf("shell-") === 0; }).map(function (k) { return caches.delete(k); })); }));
    Promise.all(jobs).catch(function () {}).then(function () { location.reload(); });
  }, 10000);
})();
