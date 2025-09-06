import { mountSidebar } from "./ui/mountSidebar";
(function bootstrap() {
  const DEMO_FLAG = document.querySelector("#codexia-claim");
  if (DEMO_FLAG) mountSidebar();
  chrome.runtime.onMessage?.addListener((msg) => { if (msg?.type === "TOGGLE_SIDEBAR") mountSidebar(); });
})();
