/*
  # Create Circuit Design Tables

  ## Tables Created
  
  1. `circuit_designs` - Main table for storing circuit design projects
     - `id` (uuid, primary key) - Unique identifier for the circuit design
     - `name` (varchar) - Name of the circuit design
     - `description` (text) - Detailed description of the design
     - `version` (varchar) - Version number of the design
     - `status` (varchar) - Current status (draft, active, archived)
     - `design_data` (jsonb) - Structured data containing the circuit design
     - `user_id` (uuid) - ID of the user who created the design
     - `created_at` (timestamp) - Timestamp when created
     - `updated_at` (timestamp) - Timestamp when last updated
  
  2. `components` - Components used in circuit designs
     - `id` (uuid, primary key) - Unique identifier for the component
     - `circuit_design_id` (uuid, foreign key) - Reference to circuit design
     - `name` (varchar) - Component name
     - `component_type` (varchar) - Type of component (resistor, capacitor, etc.)
     - `description` (text) - Component description
     - `properties` (jsonb) - Component properties and specifications
     - `position_x` (float) - X coordinate in the design
     - `position_y` (float) - Y coordinate in the design
     - `created_at` (timestamp) - Timestamp when created
     - `updated_at` (timestamp) - Timestamp when last updated
  
  3. `simulation_results` - Results from circuit simulations
     - `id` (uuid, primary key) - Unique identifier for the simulation result
     - `circuit_design_id` (uuid, foreign key) - Reference to circuit design
     - `simulation_type` (varchar) - Type of simulation run
     - `status` (varchar) - Status of the simulation (pending, running, completed, failed)
     - `success` (boolean) - Whether the simulation was successful
     - `execution_time` (float) - Time taken to execute the simulation
     - `result_data` (jsonb) - Simulation output data
     - `error_message` (text) - Error message if simulation failed
     - `created_at` (timestamp) - Timestamp when created
     - `updated_at` (timestamp) - Timestamp when last updated

  ## Security
  
  - Enable RLS on all tables
  - Add policies for authenticated users to manage their own data
  - Users can only access circuit designs they own
  - Components and simulation results are accessible through their parent circuit design

  ## Indexes
  
  - Added indexes on foreign keys for better query performance
  - Added index on circuit_designs.name for search
  - Added index on user_id for filtering by user
*/

-- Create circuit_designs table
CREATE TABLE IF NOT EXISTS circuit_designs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(255) NOT NULL,
  description text,
  version varchar(50) DEFAULT '1.0.0',
  status varchar(50) DEFAULT 'draft',
  design_data jsonb,
  user_id uuid,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_circuit_designs_name ON circuit_designs(name);
CREATE INDEX IF NOT EXISTS idx_circuit_designs_user_id ON circuit_designs(user_id);

-- Create components table
CREATE TABLE IF NOT EXISTS components (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  circuit_design_id uuid NOT NULL REFERENCES circuit_designs(id) ON DELETE CASCADE,
  name varchar(255) NOT NULL,
  component_type varchar(100) NOT NULL,
  description text,
  properties jsonb,
  position_x float,
  position_y float,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_components_circuit_design_id ON components(circuit_design_id);

-- Create simulation_results table
CREATE TABLE IF NOT EXISTS simulation_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  circuit_design_id uuid NOT NULL REFERENCES circuit_designs(id) ON DELETE CASCADE,
  simulation_type varchar(100) NOT NULL,
  status varchar(50) DEFAULT 'pending',
  success boolean DEFAULT false,
  execution_time float,
  result_data jsonb,
  error_message text,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_simulation_results_circuit_design_id ON simulation_results(circuit_design_id);

-- Enable Row Level Security
ALTER TABLE circuit_designs ENABLE ROW LEVEL SECURITY;
ALTER TABLE components ENABLE ROW LEVEL SECURITY;
ALTER TABLE simulation_results ENABLE ROW LEVEL SECURITY;

-- RLS Policies for circuit_designs
CREATE POLICY "Users can view own circuit designs"
  ON circuit_designs FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own circuit designs"
  ON circuit_designs FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own circuit designs"
  ON circuit_designs FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own circuit designs"
  ON circuit_designs FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- RLS Policies for components
CREATE POLICY "Users can view components of own circuit designs"
  ON components FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = components.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert components to own circuit designs"
  ON components FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = components.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update components of own circuit designs"
  ON components FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = components.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = components.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete components of own circuit designs"
  ON components FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = components.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

-- RLS Policies for simulation_results
CREATE POLICY "Users can view simulation results of own circuit designs"
  ON simulation_results FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = simulation_results.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert simulation results to own circuit designs"
  ON simulation_results FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = simulation_results.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update simulation results of own circuit designs"
  ON simulation_results FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = simulation_results.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = simulation_results.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete simulation results of own circuit designs"
  ON simulation_results FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM circuit_designs
      WHERE circuit_designs.id = simulation_results.circuit_design_id
      AND circuit_designs.user_id = auth.uid()
    )
  );