import { Heart } from 'lucide-react';
import { Header } from '@/components/shop/Header';
import { BottomNav } from '@/components/shop/BottomNav';
import { ProductCard } from '@/components/shop/ProductCard';
import { EmptyState } from '@/components/shop/EmptyState';
import { useFavoritesStore } from '@/stores/favoritesStore';

export default function FavoritesPage() {
  const favorites = useFavoritesStore((state) => state.items);
  
  return (
    <div className="min-h-screen bg-background">
      <Header showSearch={false} title="Избранное" />
      
      <main className="container py-4 pb-24">
        {favorites.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
            {favorites.map((product, index) => (
              <ProductCard 
                key={product.id} 
                product={product} 
                index={index}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            icon={Heart}
            title="Пока пусто"
            description="Добавляйте понравившиеся товары в избранное, нажимая на сердечко"
            actionLabel="Перейти в каталог"
            actionHref="/"
          />
        )}
      </main>

      <BottomNav />
    </div>
  );
}
