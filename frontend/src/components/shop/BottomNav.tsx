import { Link, useLocation } from 'react-router-dom';
import { Home, Heart, ShoppingBag, User } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { useCartStore } from '@/stores/cartStore';
import { useFavoritesStore } from '@/stores/favoritesStore';
import { cn } from '@/lib/utils';
import { hapticFeedback } from '@/lib/telegram';

interface NavItem {
  path: string;
  label: string;
  icon: typeof Home;
  getBadge?: () => number;
}

export function BottomNav() {
  const location = useLocation();
  const cartItemCount = useCartStore((state) => state.getItemCount());
  const favoritesCount = useFavoritesStore((state) => state.items.length);

  const navItems: NavItem[] = [
    { path: '/', label: 'Главная', icon: Home },
    { path: '/favorites', label: 'Избранное', icon: Heart, getBadge: () => favoritesCount },
    { path: '/cart', label: 'Корзина', icon: ShoppingBag, getBadge: () => cartItemCount },
    { path: '/profile', label: 'Профиль', icon: User },
  ];

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  const handleNavClick = () => {
    hapticFeedback('light');
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-md border-t border-border safe-area-bottom">
      <div className="flex items-center justify-around h-16 max-w-lg mx-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          const badge = item.getBadge?.() || 0;

          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={handleNavClick}
              className={cn(
                "flex flex-col items-center justify-center gap-1 px-4 py-2 rounded-xl transition-all relative",
                active 
                  ? "text-primary" 
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              <div className="relative">
                <Icon 
                  className={cn(
                    "h-6 w-6 transition-all",
                    active && item.path === '/favorites' && "fill-primary"
                  )} 
                  strokeWidth={active ? 2.5 : 2}
                />
                {badge > 0 && (
                  <Badge 
                    variant="default" 
                    className="absolute -top-2 -right-3 h-5 min-w-5 p-0 flex items-center justify-center text-[10px] font-semibold"
                  >
                    {badge > 99 ? '99+' : badge}
                  </Badge>
                )}
              </div>
              <span className={cn(
                "text-[10px] font-medium transition-all",
                active && "text-primary font-semibold"
              )}>
                {item.label}
              </span>
              {active && (
                <div className="absolute -bottom-1 w-1 h-1 rounded-full bg-primary" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
