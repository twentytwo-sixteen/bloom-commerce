import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Форматирование цены в рублях
 * Использует неразрывный пробел чтобы ₽ не переносился на новую строку
 */
export function formatPrice(kopecks: number): string {
  const rubles = kopecks / 100;
  const formatted = new Intl.NumberFormat('ru-RU').format(rubles);
  // \u00A0 - неразрывный пробел
  return `${formatted}\u00A0₽`;
}
