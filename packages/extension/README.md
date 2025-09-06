# Codexia Sidebar Extension

## Build

```bash
npm run build
```

## Load in Chrome

1. Go to `chrome://extensions`.
2. Enable **Developer Mode**.
3. Click **Load Unpacked** and select `packages/extension/dist`.

Note: To keep PRs text-only, icons are omitted. After merging, you can add PNG icons (16/32/48/128) to `packages/extension/public/` and re-build. Chrome will load without icons.

## Demo

Open `packages/extension/public/demo/mock.html` in Chrome (drag into a tab or serve via `file://`). Click the toolbar icon to toggle the sidebar. Use **Assess → Plan → Apply Fix** to exercise the flow.

## Troubleshooting

* Set `VITE_API_BASE` if backend is on another host.
* Ensure the backend allows CORS from the extension.
