import { useState } from 'react';
import { SlidersHorizontal, Check } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Category } from '@/types/shop';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { hapticFeedback } from '@/lib/telegram';

export type SortOption = 'default' | 'new' | 'price_asc' | 'price_desc';

interface SortOptionItem {
  value: SortOption;
  label: string;
}

const sortOptions: SortOptionItem[] = [
  { value: 'default', label: 'По умолчанию' },
  { value: 'new', label: 'Сначала новые' },
  { value: 'price_asc', label: 'Сначала дешёвые' },
  { value: 'price_desc', label: 'Сначала дорогие' },
];

interface CategoryChipsProps {
  categories: Category[];
  selectedSlug: string | null;
  onSelect: (slug: string | null) => void;
  sortBy?: SortOption;
  onSortChange?: (sort: SortOption) => void;
}

export function CategoryChips({ 
  categories, 
  selectedSlug, 
  onSelect,
  sortBy = 'default',
  onSortChange,
}: CategoryChipsProps) {
  const [isOpen, setIsOpen] = useState(false);

  const currentSort = sortOptions.find(opt => opt.value === sortBy);
  const isFiltered = sortBy !== 'default';

  const handleSortSelect = (value: SortOption) => {
    hapticFeedback('light');
    onSortChange?.(value);
    setIsOpen(false);
  };

  const handleCategorySelect = (slug: string | null) => {
    hapticFeedback('light');
    onSelect(slug);
  };

  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide -mx-4 px-4">
      {/* Filter/Sort Button */}
      {onSortChange && (
        <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
          <DropdownMenuTrigger asChild>
            <Button
              variant="outline"
              size="sm"
              className={cn(
                "flex-shrink-0 h-9 px-3 rounded-full border-border gap-1.5",
                isFiltered && "bg-primary/10 border-primary text-primary"
              )}
            >
              <SlidersHorizontal className="h-4 w-4" />
              <span className="hidden sm:inline text-sm">
                {isFiltered ? currentSort?.label : 'Фильтр'}
              </span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="w-48">
            {sortOptions.map((option) => (
              <DropdownMenuItem
                key={option.value}
                onClick={() => handleSortSelect(option.value)}
                className="flex items-center justify-between"
              >
                <span>{option.label}</span>
                {sortBy === option.value && (
                  <Check className="h-4 w-4 text-primary" />
                )}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      )}

      {/* Divider */}
      {onSortChange && (
        <div className="h-6 w-px bg-border flex-shrink-0" />
      )}

      {/* All button */}
      <button
        onClick={() => handleCategorySelect(null)}
        className={cn(
          "flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200",
          selectedSlug === null
            ? "bg-primary text-primary-foreground shadow-button"
            : "bg-muted text-muted-foreground hover:bg-muted/80"
        )}
      >
        Все
      </button>

      {/* Category chips */}
      {categories.map((category) => (
        <button
          key={category.id}
          onClick={() => handleCategorySelect(category.slug)}
          className={cn(
            "flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200",
            selectedSlug === category.slug
              ? "bg-primary text-primary-foreground shadow-button"
              : "bg-muted text-muted-foreground hover:bg-muted/80"
          )}
        >
          {category.title}
          {category.products_count !== undefined && (
            <span className="ml-1 text-xs opacity-70">
              ({category.products_count})
            </span>
          )}
        </button>
      ))}
    </div>
  );
}
