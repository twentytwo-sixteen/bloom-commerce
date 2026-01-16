import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface HeaderProps {
  onSearch?: (query: string) => void;
  showSearch?: boolean;
  title?: string;
}

export function Header({ onSearch, showSearch = true, title }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(searchQuery);
  };
  
  return (
    <header className="sticky top-0 z-50 safe-area-top bg-background/95 backdrop-blur-md border-b border-border">
      <div className="container flex h-14 items-center justify-center gap-4 relative">
        {/* Search button - left side */}
        {showSearch && (
          <Button
            variant="ghost"
            size="icon"
            className="absolute left-4"
            onClick={() => setSearchOpen(!searchOpen)}
          >
            {searchOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Search className="h-5 w-5" />
            )}
          </Button>
        )}
        
        {/* Logo - center */}
        <Link to="/" className="flex items-center gap-2">
          <span className="text-2xl">🌸</span>
          <span className="font-display text-xl font-semibold text-foreground">
            {title || 'Bloom'}
          </span>
        </Link>
      </div>
      
      {/* Mobile Search Bar */}
      {showSearch && searchOpen && (
        <div className="px-4 pb-3 animate-slide-up">
          <form onSubmit={handleSearch}>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Найти цветы..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  onSearch?.(e.target.value);
                }}
                className="pl-10 bg-muted border-0"
                autoFocus
              />
            </div>
          </form>
        </div>
      )}
    </header>
  );
}
