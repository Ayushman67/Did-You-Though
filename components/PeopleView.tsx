'use client';

import { useState } from 'react';
import { useStore } from '@/lib/store';
import { CheckCircle2, Circle, Calendar, Copy, Check } from 'lucide-react';

export default function PeopleView() {
  const { tasks, toggleTaskStatus } = useStore();
  const [selectedOwner, setSelectedOwner] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const owners = Array.from(new Set(tasks.map(t => t.owner)));

  // Auto-select first owner if none selected
  const activeOwner = selectedOwner || owners[0] || null;

  const ownerTasks = activeOwner
    ? tasks.filter(t => t.owner === activeOwner)
    : [];

  const openTasks = ownerTasks.filter(t => t.status === 'Open');
  const doneTasks = ownerTasks.filter(t => t.status === 'Done');
  const completionRate = ownerTasks.length > 0
    ? Math.round((doneTasks.length / ownerTasks.length) * 100)
    : 0;

  const generateFollowUp = () => {
    if (!activeOwner || openTasks.length === 0) return '';

    const taskList = openTasks
      .map(t => `• ${t.description} (Due: ${t.dueDate})`)
      .join('\n');

    return `Hi ${activeOwner.split(' ')[0]},

Following up on these open items:

${taskList}

Let me know if you need any support or if timelines have changed.

Thanks!`;
  };

  const copyFollowUp = () => {
    navigator.clipboard.writeText(generateFollowUp());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const priorityStyles = {
    High: 'badge-danger',
    Med: 'badge-warning',
    Low: 'badge-success',
  };

  if (owners.length === 0) {
    return (
      <div className="card p-8 text-center">
        <p className="text-text-secondary">No team members yet</p>
        <p className="text-sm text-text-muted mt-1">Process a meeting to see people here</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* People List */}
      <div className="card p-4">
        <h2 className="text-xs font-semibold text-text-muted uppercase tracking-wide px-2 mb-3">
          Team Members
        </h2>
        <div className="space-y-1">
          {owners.map((owner) => {
            const ownerTaskCount = tasks.filter(t => t.owner === owner);
            const ownerOpenCount = ownerTaskCount.filter(t => t.status === 'Open').length;
            const ownerHighCount = ownerTaskCount.filter(t => t.priority === 'High' && t.status === 'Open').length;

            return (
              <button
                key={owner}
                onClick={() => setSelectedOwner(owner)}
                className={`
                  w-full flex items-center justify-between p-3 rounded-lg
                  transition-colors duration-150 text-left
                  ${activeOwner === owner
                    ? 'bg-accent-light'
                    : 'hover:bg-gray-50'
                  }
                `}
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-accent flex items-center justify-center text-sm font-semibold text-white">
                    {owner.charAt(0)}
                  </div>
                  <div>
                    <p className={`text-sm font-medium ${
                      activeOwner === owner ? 'text-accent' : 'text-text-primary'
                    }`}>
                      {owner}
                    </p>
                    <p className="text-xs text-text-muted">{ownerOpenCount} open</p>
                  </div>
                </div>

                {ownerHighCount > 0 && (
                  <span className="badge-danger">
                    {ownerHighCount} high
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Person Detail */}
      <div className="lg:col-span-2 card p-5">
        {activeOwner && (
          <>
            {/* Header */}
            <div className="flex items-center justify-between mb-6 pb-6 border-b border-border">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-accent flex items-center justify-center text-lg font-semibold text-white">
                  {activeOwner.charAt(0)}
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-text-primary">{activeOwner}</h2>
                  <p className="text-sm text-text-muted">
                    {openTasks.length} open · {doneTasks.length} done
                  </p>
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-6">
              <div className="flex items-center justify-between text-sm mb-2">
                <span className="text-text-secondary">Completion</span>
                <span className="font-medium text-text-primary">{completionRate}%</span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-accent rounded-full transition-all duration-500"
                  style={{ width: `${completionRate}%` }}
                />
              </div>
            </div>

            {/* Tasks */}
            <div className="space-y-2 max-h-64 overflow-y-auto mb-6">
              {ownerTasks.map((task) => (
                <div
                  key={task.id}
                  onClick={() => toggleTaskStatus(task.id)}
                  className={`
                    group flex items-center gap-3 p-3 rounded-lg border cursor-pointer
                    transition-all duration-150
                    ${task.status === 'Done'
                      ? 'bg-gray-50 border-transparent'
                      : 'border-border hover:border-accent hover:shadow-sm'
                    }
                  `}
                >
                  <button className="flex-shrink-0">
                    {task.status === 'Done' ? (
                      <CheckCircle2 className="w-4.5 h-4.5 text-success" />
                    ) : (
                      <Circle className="w-4.5 h-4.5 text-text-muted group-hover:text-accent transition-colors" />
                    )}
                  </button>

                  <p className={`flex-1 text-sm truncate ${
                    task.status === 'Done'
                      ? 'text-text-muted line-through'
                      : 'text-text-primary'
                  }`}>
                    {task.description}
                  </p>

                  <span className="text-xs text-text-muted flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {task.dueDate}
                  </span>

                  <span className={priorityStyles[task.priority]}>
                    {task.priority}
                  </span>
                </div>
              ))}
            </div>

            {/* Email Draft */}
            {openTasks.length > 0 && (
              <div className="border-t border-border pt-6">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xs font-semibold text-text-muted uppercase tracking-wide">
                    Follow-up Email Draft
                  </h3>
                  <button
                    onClick={copyFollowUp}
                    className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium text-accent hover:bg-accent-light transition-colors"
                  >
                    {copied ? (
                      <>
                        <Check className="w-3.5 h-3.5" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        Copy
                      </>
                    )}
                  </button>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 text-sm text-text-secondary whitespace-pre-wrap font-mono leading-relaxed">
                  {generateFollowUp()}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
