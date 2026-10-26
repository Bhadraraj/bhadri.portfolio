(() => {
  const canvas = document.querySelector('.hero-globe');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const TAU = Math.PI * 2;
  let width = 0, height = 0, radius = 0, angle = 0, frame = 0, last = 0, visible = false;
  const nodes = Array.from({ length: 48 }, (_, i) => {
    const lat = Math.asin(1 - 2 * (i + .5) / 48);
    return { lat, lon: i * 2.399963, bright: i % 5 === 0 };
  });
  function project(lat, lon) {
    const x = Math.cos(lat) * Math.sin(lon + angle);
    const y = Math.sin(lat);
    const z = Math.cos(lat) * Math.cos(lon + angle);
    const tilt = -.23;
    return { x: width / 2 + (x * Math.cos(tilt) - y * Math.sin(tilt)) * radius,
      y: height * .53 + (x * Math.sin(tilt) + y * Math.cos(tilt)) * radius, z };
  }
  function line(points, alpha, thickness = .65) {
    ctx.lineWidth = thickness;
    for (let i = 1; i < points.length; i++) {
      const a = points[i - 1], b = points[i];
      ctx.strokeStyle = `rgba(78,132,255,${alpha * (.16 + .84 * Math.max(0, (a.z + b.z) / 2))})`;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }
  }
  function draw() {
    ctx.clearRect(0, 0, width, height);
    const glow = ctx.createRadialGradient(width * .43, height * .43, 0, width / 2, height * .53, radius * 1.15);
    glow.addColorStop(0, 'rgba(60,114,252,.12)'); glow.addColorStop(.8, 'rgba(60,114,252,.025)'); glow.addColorStop(1, 'rgba(60,114,252,0)');
    ctx.fillStyle = glow; ctx.fillRect(0, 0, width, height);
    for (let lat = -75; lat <= 75; lat += 15) {
      line(Array.from({ length: 97 }, (_, i) => project(lat * Math.PI / 180, i * TAU / 96)), .58);
    }
    for (let lon = 0; lon < 360; lon += 20) {
      line(Array.from({ length: 49 }, (_, i) => project(-Math.PI / 2 + i * Math.PI / 48, lon * Math.PI / 180)), .58);
    }
    // Sparse arcs connect points across the visible hemisphere.
    nodes.forEach((n, i) => {
      const p = project(n.lat, n.lon);
      if (p.z < .05) return;
      if (n.bright) {
        const next = nodes[(i + 7) % nodes.length];
        const q = project(next.lat, next.lon);
        if (q.z > .1) {
          ctx.strokeStyle = `rgba(123,162,255,${p.z * .35})`; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(p.x, p.y);
          ctx.quadraticCurveTo((p.x + q.x) / 2, Math.min(p.y, q.y) - radius * .2, q.x, q.y); ctx.stroke();
        }
      }
      ctx.shadowColor = '#3c72fc'; ctx.shadowBlur = n.bright ? 15 : 5;
      ctx.fillStyle = `rgba(${n.bright ? '195,216,255' : '85,143,255'},${.25 + p.z * .75})`;
      ctx.beginPath(); ctx.arc(p.x, p.y, n.bright ? 2.6 : 1.4, 0, TAU); ctx.fill(); ctx.shadowBlur = 0;
    });
    ctx.strokeStyle = 'rgba(89,143,255,.48)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(width / 2, height * .53, radius, 0, TAU); ctx.stroke();
  }
  function animate(time) {
    angle += Math.min(time - (last || time), 50) * .0001;
    last = time; draw(); frame = requestAnimationFrame(animate);
  }
  function sync() {
    cancelAnimationFrame(frame); last = 0;
    if (visible && !document.hidden && !motion.matches) frame = requestAnimationFrame(animate);
    else draw();
  }
  new ResizeObserver(() => {
    width = canvas.clientWidth; height = canvas.clientHeight;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    radius = Math.min(width * .395, height * .39); draw();
  }).observe(canvas);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }).observe(canvas);
  motion.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
})();
