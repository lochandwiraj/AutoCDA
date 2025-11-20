'use client';

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Component } from './component-library-browser';

interface ComponentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (component: Component) => void;
  editingComponent: Component | null;
}

export function ComponentModal({
  isOpen,
  onClose,
  onSubmit,
  editingComponent,
}: ComponentModalProps) {
  const [formData, setFormData] = useState<Component>({
    id: '',
    type: '',
    value: '',
    footprint: '',
    datasheet: '',
  });

  useEffect(() => {
    if (editingComponent) {
      setFormData(editingComponent);
    } else {
      setFormData({
        id: '',
        type: '',
        value: '',
        footprint: '',
        datasheet: '',
      });
    }
  }, [editingComponent, isOpen]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (
      formData.id &&
      formData.type &&
      formData.value &&
      formData.footprint &&
      formData.datasheet
    ) {
      onSubmit(formData);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>
            {editingComponent ? 'Edit Component' : 'Add New Component'}
          </DialogTitle>
          <DialogDescription>
            {editingComponent
              ? 'Update the component details below.'
              : 'Fill in the component information to add it to the library.'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="id">Component ID</Label>
            <Input
              id="id"
              name="id"
              value={formData.id}
              onChange={handleChange}
              placeholder="e.g., R001"
              disabled={!!editingComponent}
            />
          </div>

          <div>
            <Label htmlFor="type">Type</Label>
            <Input
              id="type"
              name="type"
              value={formData.type}
              onChange={handleChange}
              placeholder="e.g., Resistor"
            />
          </div>

          <div>
            <Label htmlFor="value">Value</Label>
            <Input
              id="value"
              name="value"
              value={formData.value}
              onChange={handleChange}
              placeholder="e.g., 10kΩ"
            />
          </div>

          <div>
            <Label htmlFor="footprint">Footprint</Label>
            <Input
              id="footprint"
              name="footprint"
              value={formData.footprint}
              onChange={handleChange}
              placeholder="e.g., 0805"
            />
          </div>

          <div>
            <Label htmlFor="datasheet">Datasheet Link</Label>
            <Input
              id="datasheet"
              name="datasheet"
              type="url"
              value={formData.datasheet}
              onChange={handleChange}
              placeholder="https://example.com/datasheet.pdf"
            />
          </div>

          <div className="flex justify-end gap-2 pt-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit">
              {editingComponent ? 'Update' : 'Add'} Component
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
