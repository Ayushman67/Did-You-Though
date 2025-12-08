'use client';

import { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import MeetingInput from '@/components/MeetingInput';
import TaskList from '@/components/TaskList';
import StatsCards from '@/components/StatsCards';
import Charts from '@/components/Charts';
import PeopleView from '@/components/PeopleView';
import MeetingLog from '@/components/MeetingLog';
import CompletionToast from '@/components/CompletionToast';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'home' | 'people' | 'meetings'>('home');

  return (
    <div className="flex h-screen bg-background">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      
      <main className="flex-1 overflow-auto">
        <div className="max-w-5xl mx-auto px-8 py-6">
          <Header />
          
          {activeTab === 'home' && (
            <div className="space-y-6 animate-fade-in">
              <StatsCards />
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <MeetingInput />
                <TaskList />
              </div>
              
              <Charts />
            </div>
          )}
          
          {activeTab === 'people' && (
            <div className="animate-fade-in">
              <PeopleView />
            </div>
          )}
          
          {activeTab === 'meetings' && (
            <div className="animate-fade-in">
              <MeetingLog />
            </div>
          )}
        </div>
      </main>
      
      <CompletionToast />
    </div>
  );
}
