'use client';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Component } from './component-library-browser';
import { MoreHorizontal, Edit2, Trash2, ExternalLink } from 'lucide-react';

interface ComponentsTableProps {
  components: Component[];
  onEdit: (component: Component) => void;
  onDelete: (id: string) => void;
}

export function ComponentsTable({
  components,
  onEdit,
  onDelete,
}: ComponentsTableProps) {
  if (components.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-card p-8 text-center">
        <p className="text-muted-foreground">
          No components found. Try adjusting your search filters.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <Table>
        <TableHeader>
          <TableRow className="border-border bg-muted hover:bg-muted">
            <TableHead className="font-semibold">Component ID</TableHead>
            <TableHead className="font-semibold">Type</TableHead>
            <TableHead className="font-semibold">Value</TableHead>
            <TableHead className="font-semibold">Footprint</TableHead>
            <TableHead className="font-semibold">Datasheet</TableHead>
            <TableHead className="w-12 text-right font-semibold">
              Actions
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {components.map((component) => (
            <TableRow key={component.id} className="border-border hover:bg-muted/50">
              <TableCell className="font-medium text-foreground">
                {component.id}
              </TableCell>
              <TableCell className="text-foreground">{component.type}</TableCell>
              <TableCell className="text-foreground">{component.value}</TableCell>
              <TableCell className="text-foreground">
                {component.footprint}
              </TableCell>
              <TableCell>
                <a
                  href={component.datasheet}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-primary hover:underline"
                >
                  <span className="hidden sm:inline">View</span>
                  <ExternalLink className="h-4 w-4" />
                </a>
              </TableCell>
              <TableCell className="text-right">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                      <MoreHorizontal className="h-4 w-4" />
                      <span className="sr-only">Open menu</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => onEdit(component)}>
                      <Edit2 className="mr-2 h-4 w-4" />
                      Edit
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() => onDelete(component.id)}
                      className="text-destructive focus:text-destructive"
                    >
                      <Trash2 className="mr-2 h-4 w-4" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
