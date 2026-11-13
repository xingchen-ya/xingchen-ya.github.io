const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const viewer = document.querySelector(".image-viewer");
const galleryLinks = [...document.querySelectorAll(".project-visual a")];
const viewerImage = viewer.querySelector(".viewer-image");
const viewerStage = viewer.querySelector(".viewer-stage");
const viewerStatus = viewer.querySelector(".viewer-status");
const viewerTitle = viewer.querySelector("#viewer-title");
const viewerCount = viewer.querySelector("#viewer-count");
const originalLink = viewer.querySelector(".viewer-original");
let currentGroup = [];
let currentIndex = 0;
let opener;

function showImage(index) {
  currentIndex = (index + currentGroup.length) % currentGroup.length;
  const link = currentGroup[currentIndex];
  const thumbnail = link.querySelector("img");
  viewerTitle.textContent = link.closest(".project").querySelector("h3").firstChild.textContent.trim();
  viewerCount.textContent = `${currentIndex + 1} / ${currentGroup.length} · ${thumbnail.alt}`;
  viewerImage.alt = thumbnail.alt;
  originalLink.href = link.href;
  viewerStage.classList.remove("has-error");
  viewerStage.classList.add("is-loading");
  viewerStatus.textContent = "正在加载图片…";
  viewerImage.src = link.href;
}

viewerImage.addEventListener("load", () => {
  viewerStage.classList.remove("is-loading");
  viewerStatus.textContent = "";
});
viewerImage.addEventListener("error", () => {
  viewerStage.classList.remove("is-loading");
  viewerStage.classList.add("has-error");
  viewerStatus.textContent = "图片暂时无法加载，可重试或打开原图。";
});

for (const link of galleryLinks) {
  link.addEventListener("click", (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey ||
        typeof viewer.showModal !== "function") return;
    event.preventDefault();
    opener = link;
    currentGroup = [...link.closest(".project-visual").querySelectorAll("a")];
    showImage(currentGroup.indexOf(link));
    viewer.showModal();
    document.body.classList.add("viewer-open");
  });
}
viewer.querySelector("[data-previous]").addEventListener("click", () => showImage(currentIndex - 1));
viewer.querySelector("[data-next]").addEventListener("click", () => showImage(currentIndex + 1));
viewer.addEventListener("keydown", (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey) return;
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    showImage(currentIndex + (event.key === "ArrowLeft" ? -1 : 1));
  }
});
viewer.addEventListener("click", (event) => {
  if (event.target !== viewer) return;
  const bounds = viewer.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
});
viewer.addEventListener("close", () => {
  document.body.classList.remove("viewer-open");
  opener?.focus({ preventScroll: true });
});

for (const details of document.querySelectorAll(".project details")) {
  details.addEventListener("toggle", () => {
    if (details.open && !reducedMotion.matches) {
      details.querySelector("dl").animate(
        [{ opacity: 0, transform: "translateY(4px)" }, { opacity: 1, transform: "none" }],
        { duration: 180, easing: "ease-out" }
      );
    }
  });
}

const sectionLinks = [...document.querySelectorAll('nav a[href^="#"]')];
let navigationFrame = 0;
function updateNavigation() {
  navigationFrame = 0;
  let activeLink;
  let activeTop = -Infinity;
  const activationTop = Math.min(96, window.innerHeight * 0.38);
  for (const link of sectionLinks) {
    const top = document.querySelector(link.hash).getBoundingClientRect().top;
    const isHashTie = Math.abs(top - activeTop) < 1 && link.hash === window.location.hash;
    if (top <= activationTop && (top > activeTop || isHashTie)) {
      activeLink = link;
      activeTop = top;
    }
  }
  // Short closing sections cannot always reach the usual activation line.
  if (window.scrollY > 0 &&
      window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
    activeLink = sectionLinks.at(-1);
  }
  for (const link of sectionLinks) {
    if (link === activeLink) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}
function scheduleNavigation() {
  if (!navigationFrame) navigationFrame = requestAnimationFrame(updateNavigation);
}
window.addEventListener("scroll", scheduleNavigation, { passive: true });
window.addEventListener("resize", scheduleNavigation);
window.addEventListener("hashchange", scheduleNavigation);
updateNavigation();
