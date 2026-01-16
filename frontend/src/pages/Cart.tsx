import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBag, Tag, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Header } from '@/components/shop/Header';
import { BottomNav } from '@/components/shop/BottomNav';
import { CartItemComponent } from '@/components/shop/CartItem';
import { EmptyState } from '@/components/shop/EmptyState';
import { useCartStore } from '@/stores/cartStore';
import { hapticFeedback } from '@/lib/telegram';
import { toast } from 'sonner';
import { formatPrice } from '@/lib/utils';

// Mock promo codes (fixed_amount in kopecks)
const promoCodes = {
  'BLOOM10': { code: 'BLOOM10', discount_percent: 10, is_active: true },
  'SALE500': { code: 'SALE500', fixed_amount: 50000, is_active: true }, // 500 руб в копейках
};

export default function CartPage() {
  const [promoInput, setPromoInput] = useState('');
  const [promoLoading, setPromoLoading] = useState(false);
  
  const { 
    items, 
    promoCode, 
    applyPromo, 
    removePromo,
    getSubtotal,
    getDiscount,
    getTotal 
  } = useCartStore();
  
  const handleApplyPromo = async () => {
    if (!promoInput.trim()) return;
    
    setPromoLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const promo = promoCodes[promoInput.toUpperCase() as keyof typeof promoCodes];
    
    if (promo && promo.is_active) {
      applyPromo(promo);
      setPromoInput('');
      hapticFeedback('success');
      toast.success('Промокод применён');
    } else {
      hapticFeedback('error');
      toast.error('Промокод не найден или истёк');
    }
    
    setPromoLoading(false);
  };
  
  const handleRemovePromo = () => {
    removePromo();
    hapticFeedback('light');
  };
  
  const subtotal = getSubtotal();
  const discount = getDiscount();
  const total = getTotal();
  
  return (
    <div className="min-h-screen bg-background">
      <Header showSearch={false} title="Корзина" />
      
      <main className="container py-4 pb-48">
        {items.length > 0 ? (
          <>
            {/* Cart Items */}
            <div className="space-y-3 mb-6">
              {items.map((item, index) => (
                <CartItemComponent 
                  key={item.product_id} 
                  item={item} 
                  index={index}
                />
              ))}
            </div>
            
            {/* Promo Code */}
            <div className="bg-card rounded-xl p-4 shadow-card mb-6">
              <h3 className="font-medium text-foreground mb-3 flex items-center gap-2">
                <Tag className="h-4 w-4" />
                Промокод
              </h3>
              
              {promoCode ? (
                <div className="flex items-center justify-between bg-accent/10 rounded-lg px-4 py-3">
                  <div>
                    <span className="font-medium text-accent">{promoCode.code}</span>
                    <p className="text-sm text-muted-foreground">
                      Скидка: {formatPrice(discount)}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleRemovePromo}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ) : (
                <div className="flex gap-2">
                  <Input
                    placeholder="Введите промокод"
                    value={promoInput}
                    onChange={(e) => setPromoInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleApplyPromo()}
                    className="bg-muted border-0"
                  />
                  <Button
                    variant="secondary"
                    onClick={handleApplyPromo}
                    disabled={promoLoading || !promoInput.trim()}
                  >
                    {promoLoading ? '...' : 'Применить'}
                  </Button>
                </div>
              )}
            </div>
          </>
        ) : (
          <EmptyState
            icon={ShoppingBag}
            title="Корзина пуста"
            description="Добавьте что-нибудь из каталога, чтобы оформить заказ"
            actionLabel="Перейти в каталог"
            actionHref="/"
          />
        )}
      </main>
      
      {/* Bottom Summary */}
      {items.length > 0 && (
        <div className="fixed bottom-16 left-0 right-0 safe-area-bottom bg-background border-t border-border">
          <div className="container py-4 space-y-3">
            {/* Summary */}
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Товары</span>
                <span>{formatPrice(subtotal)}</span>
              </div>
              {discount > 0 && (
                <div className="flex justify-between text-accent">
                  <span>Скидка</span>
                  <span>-{formatPrice(discount)}</span>
                </div>
              )}
              <div className="flex justify-between text-lg font-semibold pt-2 border-t border-border">
                <span>Итого</span>
                <span>{formatPrice(total)}</span>
              </div>
            </div>
            
            {/* Checkout Button */}
            <Button 
              size="lg" 
              className="w-full h-12"
              asChild
            >
              <Link to="/checkout">
                Оформить заказ
              </Link>
            </Button>
          </div>
        </div>
      )}

      <BottomNav />
    </div>
  );
}
