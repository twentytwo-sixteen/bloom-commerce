/**
 * React Query хуки для работы с товарами
 */
import { useQuery } from '@tanstack/react-query';
import { productsApi } from '@/lib/api';
import type { ProductsFilter } from '@/types/shop';

// Query keys
export const productKeys = {
  all: ['products'] as const,
  lists: () => [...productKeys.all, 'list'] as const,
  list: (filters?: ProductsFilter) => [...productKeys.lists(), filters] as const,
  details: () => [...productKeys.all, 'detail'] as const,
  detail: (slug: string) => [...productKeys.details(), slug] as const,
  categories: ['categories'] as const,
  category: (slug: string) => [...productKeys.categories, slug] as const,
};

/**
 * Получить список категорий
 */
export function useCategories() {
  return useQuery({
    queryKey: productKeys.categories,
    queryFn: productsApi.getCategories,
    staleTime: 5 * 60 * 1000, // 5 минут
  });
}

/**
 * Получить категорию по slug
 */
export function useCategory(slug: string) {
  return useQuery({
    queryKey: productKeys.category(slug),
    queryFn: () => productsApi.getCategory(slug),
    enabled: !!slug,
  });
}

/**
 * Получить список товаров с фильтрацией
 */
export function useProducts(filters?: ProductsFilter) {
  return useQuery({
    queryKey: productKeys.list(filters),
    queryFn: () => productsApi.getProducts(filters),
    staleTime: 2 * 60 * 1000, // 2 минуты
  });
}

/**
 * Получить товар по slug
 */
export function useProduct(slug: string) {
  return useQuery({
    queryKey: productKeys.detail(slug),
    queryFn: () => productsApi.getProduct(slug),
    enabled: !!slug,
  });
}
