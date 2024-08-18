# Table Component

## Overview
The Table component is a React-based, customizable data table with sorting, pagination, optional searching, and row selection capabilities. It uses Daisy UI classes for styling.

## Usage
```jsx
import Table from './components/Table';

const MyComponent = () => {
  const data = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User' },
  ];

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role' },
  ];

  return <Table data={data} columns={columns} itemsPerPage={5} showSearch={true} />;
};
```

## Props
| Prop            | Type     | Default  | Description                              |
| --------------- | -------- | -------- | ---------------------------------------- |
| `data`          | Array    | Required | Array of objects to display in the table |
| `columns`       | Array    | Required | Array of column definition objects       |
| `itemsPerPage`  | Number   | 10       | Number of items to display per page      |
| `onRowClick`    | Function | -        | Function called when a row is clicked    |
| `customClasses` | Object   | {}       | Custom CSS classes for table elements    |
| `loading`       | Boolean  | false    | Whether to show loading state            |
| `showSearch`    | Boolean  | true     | Whether to display the search bar        |

## Features
- Sortable columns
- Pagination
- Optional search functionality
- Row selection
- Custom column rendering
- Loading state
- Empty state handling
- Customizable styling

## Examples

### Basic Usage with Search Disabled
```jsx
<Table
  data={data}
  columns={columns}
  showSearch={false}
/>
```

### Custom Styling
```jsx
<Table
  data={data}
  columns={columns}
  customClasses={{
    wrapper: 'shadow-lg',
    table: 'bg-base-100',
    th: 'text-primary',
    td: 'text-sm',
  }}
/>
```

### Custom Column Rendering
```jsx
const columns = [
  { key: 'id', label: 'ID' },
  { 
    key: 'role', 
    label: 'Role',
    render: (value) => (
      <span className={`badge ${value === 'Admin' ? 'badge-primary' : 'badge-secondary'}`}>
        {value}
      </span>
    )
  },
];
```

## Search Functionality
By default, the search bar is displayed and allows filtering across all columns. To disable the search functionality, set the `showSearch` prop to `false`:

```jsx
<Table data={data} columns={columns} showSearch={false} />
```

When the search bar is hidden, the table will display all data without filtering.

For more detailed information, please refer to the source code and inline comments in `src/components/Table.jsx`.