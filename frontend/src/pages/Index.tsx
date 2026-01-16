import { useState } from 'react';
import { Header } from '@/components/shop/Header';
import { BottomNav } from '@/components/shop/BottomNav';
import { CategoryChips, SortOption } from '@/components/shop/CategoryChips';
import { ProductCard } from '@/components/shop/ProductCard';
import { useProducts, useCategories } from '@/hooks/useProducts';
import { Skeleton } from '@/components/ui/skeleton';

const sortToOrdering: Record<SortOption, string | undefined> = {
  default: undefined,
  new: '-created_at',
  price_asc: 'price',
  price_desc: '-price',
};

const Index = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('default');

  // Fetch data from API
  const { data: categoriesData, isLoading: categoriesLoading } = useCategories();
  const { data: productsData, isLoading: productsLoading } = useProducts({
    category: selectedCategory || undefined,
    search: searchQuery || undefined,
    ordering: sortToOrdering[sortBy],
  });

  const categories = categoriesData || [];
  const products = productsData?.results || [];

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header onSearch={handleSearch} />

      <main className="container py-4 pb-24">
        {/* Hero Section */}
        <section className="mb-6">
          <div className="bg-primary/10 rounded-2xl p-6 text-center">
            <h1 className="font-display text-2xl sm:text-3xl md:text-4xl font-bold text-primary mb-2">
              Цветы с доставкой
            </h1>
            <p className="text-muted-foreground text-sm sm:text-base">
              Свежие букеты для любого повода
            </p>
          </div>
        </section>

        {/* Categories & Filter */}
        <section className="mb-4">
          {categoriesLoading ? (
            <div className="flex gap-2 overflow-x-auto pb-2 -mx-4 px-4">
              <Skeleton className="h-9 w-20 rounded-full flex-shrink-0" />
              <div className="h-6 w-px bg-border flex-shrink-0" />
              {[...Array(4)].map((_, i) => (
                <Skeleton key={i} className="h-9 w-24 rounded-full flex-shrink-0" />
              ))}
            </div>
          ) : (
            <CategoryChips
              categories={categories}
              selectedSlug={selectedCategory}
              onSelect={setSelectedCategory}
              sortBy={sortBy}
              onSortChange={setSortBy}
            />
          )}
        </section>

        {/* Products Grid */}
        <section>
          {productsLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="bg-card rounded-2xl overflow-hidden shadow-card">
                  <Skeleton className="aspect-square" />
                  <div className="p-3 sm:p-4 space-y-2">
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-1/2" />
                  </div>
                </div>
              ))}
            </div>
          ) : products.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
              {products.map((product, index) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  index={index}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-muted-foreground">
                {searchQuery
                  ? 'По вашему запросу ничего не найдено'
                  : 'В этой категории пока нет товаров'}
              </p>
            </div>
          )}
        </section>

        {/* Pagination info */}
        {productsData && productsData.count > 0 && (
          <div className="mt-6 text-center text-sm text-muted-foreground">
            Показано {products.length} из {productsData.count} товаров
          </div>
        )}
      </main>

      <BottomNav />
    </div>
  );
};

export default Index;
