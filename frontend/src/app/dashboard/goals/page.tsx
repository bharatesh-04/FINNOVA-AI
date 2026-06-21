'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

export default function GoalsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-primary-text">Savings Goals</h1>
        <Button variant="primary">
          <Plus size={18} />
          Add Goal
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Empty state */}
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-secondary-text py-8">
              No goals yet. Create your first savings goal!
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
