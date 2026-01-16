import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { initTelegramWebApp } from "./lib/telegram";

// Инициализируем Telegram WebApp ДО рендера React
// чтобы цвета установились как можно раньше
initTelegramWebApp();

createRoot(document.getElementById("root")!).render(<App />);
