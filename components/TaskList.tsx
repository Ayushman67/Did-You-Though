'use client';

import { useState } from 'react';
import { useStore } from '@/lib/store';
import { CheckCircle2, Circle, User, Calendar, ChevronDown } from 'lucide-react';

export default function TaskList() {
  const { tasks, toggleTaskStatus } = useStore();
  const [statusFilter, setStatusFilter] = useState<'Open' | 'Done' | 'all'>('Open');
  const [ownerFilter, setOwnerFilter] = useState<string>('all');
  const [showOwnerDropdown, setShowOwnerDropdown] = useState(false);

  const owners = Array.from(new Set(tasks.map(t => t.owner)));

  const filteredTasks = tasks.filter(t => {
    if (statusFilter !== 'all' && t.status !== statusFilter) return false;
    if (ownerFilter !== 'all' && t.owner !== ownerFilter) return false;
    return true;
  });

  const priorityStyles = {
    High: 'badge-danger',
    Med: 'badge-warning',
    Low: 'badge-success',
  };

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent-light flex items-center justify-center">
            <CheckCircle2 className="w-4 h-4 text-accent" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-text-primary">Tasks</h2>
            <p className="text-xs text-text-muted">{filteredTasks.length} items</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-4">
        {/* Status Filter */}
        <div className="flex gap-1 p-1 bg-gray-50 rounded-lg">
          {(['Open', 'Done', 'all'] as const).map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors ${
                statusFilter === status
                  ? 'bg-white text-text-primary shadow-sm'
                  : 'text-text-secondary hover:text-text-primary'
              }`}
            >
              {status === 'all' ? 'All' : status}
            </button>
          ))}
        </div>

        {/* Owner Filter */}
        <div className="relative">
          <button
            onClick={() => setShowOwnerDropdown(!showOwnerDropdown)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border text-xs font-medium text-text-secondary hover:bg-gray-50 transition-colors"
          >
            <User className="w-3.5 h-3.5" />
            {ownerFilter === 'all' ? 'All owners' : ownerFilter}
            <ChevronDown className="w-3 h-3" />
          </button>

          {showOwnerDropdown && (
            <div className="absolute top-full left-0 mt-1 w-48 bg-surface border border-border rounded-lg shadow-lg z-10 py-1">
              {owners.map((owner) => (
                <button
                  key={owner}
                  onClick={() => {
                    setOwnerFilter(owner);
                    setShowOwnerDropdown(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-xs hover:bg-gray-50 transition-colors ${
                    ownerFilter === owner ? 'text-accent font-medium' : 'text-text-secondary'
                  }`}
                >
                  {owner === 'all' ? 'All owners' : owner}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-2 max-h-80 overflow-y-auto">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-sm text-text-muted">No tasks yet</p>
            <p className="text-xs text-text-muted mt-1">Process a meeting to extract tasks</p>
          </div>
        ) : (
          filteredTasks.map((task) => (
            <div
              key={task.id}
              onClick={() => toggleTaskStatus(task.id)}
              className={`
                group flex items-start gap-3 p-3 rounded-lg border cursor-pointer
                transition-all duration-150
                ${task.status === 'Done'
                  ? 'bg-gray-50 border-transparent'
                  : 'border-border hover:border-accent hover:shadow-sm'
                }
              `}
            >
              <button className="mt-0.5 flex-shrink-0">
                {task.status === 'Done' ? (
                  <CheckCircle2 className="w-4.5 h-4.5 text-success" />
                ) : (
                  <Circle className="w-4.5 h-4.5 text-text-muted group-hover:text-accent transition-colors" />
                )}
              </button>

              <div className="flex-1 min-w-0">
                <p className={`text-sm ${
                  task.status === 'Done' 
                    ? 'text-text-muted line-through' 
                    : 'text-text-primary'
                }`}>
                  {task.description}
                </p>
                <div className="flex items-center gap-3 mt-1.5 text-xs text-text-muted">
                  <span className="flex items-center gap-1">
                    <User className="w-3 h-3" />
                    {task.owner}
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {task.dueDate}
                  </span>
                </div>
              </div>

              <span className={priorityStyles[task.priority]}>
                {task.priority}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
