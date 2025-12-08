'use client';

import { useStore } from '@/lib/store';
import { 
  Home, 
  Users, 
  Calendar, 
  Trash2, 
  CheckCircle2,
  Flame
} from 'lucide-react';

interface SidebarProps {
  activeTab: 'home' | 'people' | 'meetings';
  onTabChange: (tab: 'home' | 'people' | 'meetings') => void;
}

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const { tasks, clearAllData } = useStore();
  
  const openTasks = tasks.filter(t => t.status === 'Open').length;
  const doneTasks = tasks.filter(t => t.status === 'Done').length;
  const completionRate = tasks.length > 0 
    ? Math.round((doneTasks / tasks.length) * 100) 
    : 0;

  const navItems = [
    { id: 'home' as const, label: 'Home', icon: Home },
    { id: 'people' as const, label: 'People', icon: Users },
    { id: 'meetings' as const, label: 'Meetings', icon: Calendar },
  ];

  return (
    <aside className="w-60 border-r border-border bg-surface flex flex-col">
      {/* Logo */}
      <div className="p-5 border-b border-border">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
            <Flame className="w-4.5 h-4.5 text-white" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-text-primary">DidYouThough?</h1>
            <p className="text-xs text-text-muted">Accountability Engine</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3">
        <div className="space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`
                w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium
                transition-colors duration-150
                ${activeTab === item.id 
                  ? 'bg-accent-light text-accent' 
                  : 'text-text-secondary hover:bg-gray-50 hover:text-text-primary'
                }
              `}
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Progress Section */}
      <div className="p-4 border-t border-border">
        <div className="mb-4">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="text-text-secondary font-medium">Progress</span>
            <span className="text-text-primary font-semibold">{completionRate}%</span>
          </div>
          <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div 
              className="h-full bg-accent rounded-full transition-all duration-500"
              style={{ width: `${completionRate}%` }}
            />
          </div>
        </div>

        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5 text-text-secondary">
            <div className="w-2 h-2 rounded-full bg-warning" />
            <span>{openTasks} open</span>
          </div>
          <div className="flex items-center gap-1.5 text-text-secondary">
            <CheckCircle2 className="w-3.5 h-3.5 text-success" />
            <span>{doneTasks} done</span>
          </div>
        </div>
      </div>

      {/* Clear Data */}
      <div className="p-3 border-t border-border">
        <button
          onClick={clearAllData}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-xs text-text-muted hover:text-danger hover:bg-danger-light transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          Clear all data
        </button>
      </div>
    </aside>
  );
}
