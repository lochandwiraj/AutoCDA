'use client';

import { useState, useMemo } from 'react';
import { SearchBar } from './search-bar';
import { ComponentsTable } from './components-table';
import { ComponentModal } from './component-modal';
import { Button } from '@/components/ui/button';
import { Download } from 'lucide-react';

export interface Component {
  id: string;
  type: string;
  value: string;
  footprint: string;
  datasheet: string;
}

const SAMPLE_COMPONENTS: Component[] = [
  {
    id: 'R001',
    type: 'Resistor',
    value: '10kΩ',
    footprint: '0805',
    datasheet: 'https://example.com/r001.pdf',
  },
  {
    id: 'C001',
    type: 'Capacitor',
    value: '100nF',
    footprint: '0603',
    datasheet: 'https://example.com/c001.pdf',
  },
  {
    id: 'L001',
    type: 'Inductor',
    value: '10μH',
    footprint: '0603',
    datasheet: 'https://example.com/l001.pdf',
  },
  {
    id: 'D001',
    type: 'Diode',
    value: '1N4148',
    footprint: 'SOD323',
    datasheet: 'https://example.com/d001.pdf',
  },
  {
    id: 'IC001',
    type: 'Microcontroller',
    value: 'ATmega328P',
    footprint: 'TQFP32',
    datasheet: 'https://example.com/ic001.pdf',
  },
  {
    id: 'R002',
    type: 'Resistor',
    value: '1kΩ',
    footprint: '0603',
    datasheet: 'https://example.com/r002.pdf',
  },
];

export function ComponentLibraryBrowser() {
  const [components, setComponents] = useState<Component[]>(SAMPLE_COMPONENTS);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [valueRange, setValueRange] = useState<{ min: string; max: string }>({
    min: '',
    max: '',
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingComponent, setEditingComponent] = useState<Component | null>(null);

  // Get unique types for filter dropdown
  const uniqueTypes = useMemo(() => {
    return Array.from(new Set(components.map((c) => c.type))).sort();
  }, [components]);

  // Filter components based on search and filters
  const filteredComponents = useMemo(() => {
    return components.filter((component) => {
      const matchesSearch =
        component.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        component.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
        component.value.toLowerCase().includes(searchTerm.toLowerCase()) ||
        component.footprint.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesType = !selectedType || component.type === selectedType;

      // Basic value range filtering (assuming numeric values)
      const matchesRange = true; // Simplified for demo

      return matchesSearch && matchesType && matchesRange;
    });
  }, [components, searchTerm, selectedType, valueRange]);

  const handleAddComponent = (component: Component) => {
    if (editingComponent) {
      setComponents(
        components.map((c) => (c.id === editingComponent.id ? component : c))
      );
    } else {
      setComponents([...components, component]);
    }
    setIsModalOpen(false);
    setEditingComponent(null);
  };

  const handleEditComponent = (component: Component) => {
    setEditingComponent(component);
    setIsModalOpen(true);
  };

  const handleDeleteComponent = (id: string) => {
    setComponents(components.filter((c) => c.id !== id));
  };

  const handleExportCSV = () => {
    const headers = ['Component ID', 'Type', 'Value', 'Footprint', 'Datasheet'];
    const rows = filteredComponents.map((c) => [
      c.id,
      c.type,
      c.value,
      c.footprint,
      c.datasheet,
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((row) => row.map((cell) => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'components.csv';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleOpenModal = () => {
    setEditingComponent(null);
    setIsModalOpen(true);
  };

  return (
    <div className="flex flex-col gap-6 p-6">
      {/* Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-foreground">Component Library</h1>
        <p className="text-muted-foreground">
          Manage and search your electronic components inventory
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div className="flex-1 md:max-w-2xl">
          <SearchBar
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            selectedType={selectedType}
            onTypeChange={setSelectedType}
            types={uniqueTypes}
            valueRange={valueRange}
            onValueRangeChange={setValueRange}
          />
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={handleExportCSV}
            className="flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Export CSV
          </Button>
          <Button onClick={handleOpenModal}>Add Component</Button>
        </div>
      </div>

      {/* Table */}
      <ComponentsTable
        components={filteredComponents}
        onEdit={handleEditComponent}
        onDelete={handleDeleteComponent}
      />

      {/* Modal */}
      <ComponentModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingComponent(null);
        }}
        onSubmit={handleAddComponent}
        editingComponent={editingComponent}
      />
    </div>
  );
}
