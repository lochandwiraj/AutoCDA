'use client';

import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Search } from 'lucide-react';

interface SearchBarProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
  selectedType: string;
  onTypeChange: (type: string) => void;
  types: string[];
  valueRange: { min: string; max: string };
  onValueRangeChange: (range: { min: string; max: string }) => void;
}

export function SearchBar({
  searchTerm,
  onSearchChange,
  selectedType,
  onTypeChange,
  types,
}: SearchBarProps) {
  return (
    <div className="flex flex-col gap-3">
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search by Component ID, Type, Value, or Footprint..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label className="text-sm font-medium text-foreground">
            Component Type
          </label>

          <Select
            value={selectedType === '' ? 'all' : selectedType}
            onValueChange={(val) => onTypeChange(val === 'all' ? '' : val)}
          >
            <SelectTrigger className="mt-1">
              <SelectValue placeholder="All Types" />
            </SelectTrigger>

            <SelectContent>
              {/* FIX: value cannot be "" */}
              <SelectItem value="all">All Types</SelectItem>

              {types.map((type) => (
                <SelectItem key={type} value={type}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}
