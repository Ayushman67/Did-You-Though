import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Task {
  id: string;
  description: string;
  owner: string;
  dueDate: string;
  priority: 'High' | 'Med' | 'Low';
  initiative: string;
  status: 'Open' | 'Done';
  sourceMeeting: string;
  createdAt: string;
}

export interface Meeting {
  id: string;
  date: string;
  name: string;
  type: 'text' | 'audio';
  decisions: string[];
  risks: string[];
}

interface AppState {
  tasks: Task[];
  meetings: Meeting[];
  justCompleted: string | null;
  addTasks: (tasks: Task[]) => void;
  addMeeting: (meeting: Meeting) => void;
  toggleTaskStatus: (taskId: string) => void;
  clearJustCompleted: () => void;
  clearAllData: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      tasks: [],
      meetings: [],
      justCompleted: null,

      addTasks: (newTasks) =>
        set((state) => ({
          tasks: [...state.tasks, ...newTasks],
        })),

      addMeeting: (meeting) =>
        set((state) => ({
          meetings: [meeting, ...state.meetings],
        })),

      toggleTaskStatus: (taskId) =>
        set((state) => {
          const task = state.tasks.find((t) => t.id === taskId);
          const wasOpen = task?.status === 'Open';
          return {
            tasks: state.tasks.map((t) =>
              t.id === taskId
                ? { ...t, status: t.status === 'Open' ? 'Done' : 'Open' }
                : t
            ),
            justCompleted: wasOpen ? task?.description || null : null,
          };
        }),

      clearJustCompleted: () => set({ justCompleted: null }),

      clearAllData: () => set({ tasks: [], meetings: [], justCompleted: null }),
    }),
    {
      name: 'didyouthough-storage',
    }
  )
);
